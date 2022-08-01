import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime

USERNAME_SYSTEM = '*system*'

# QuizConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class QuizConsumer( AsyncWebsocketConsumer ):

    # ルーム管理（インスタンス変数ではなく、インスタンス間で使用可能なクラス変数）
    rooms = None

    # コンストラクタ
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        # クラス変数の初期化（最初のインスタンスが生成されたときのみ実施する）
        if QuizConsumer.rooms is None:
            QuizConsumer.rooms = {} # 空の連想配列
        self.strGroupName = ''
        self.strUserName = ''
        self.strRoleType = ''

    # WebSocket接続時の処理
    async def connect( self ):
        # WebSocket接続を受け入れます。
        # ・connect()でaccept()を呼び出さないと、接続は拒否されて閉じられます。
        # 　たとえば、要求しているユーザーが要求されたアクションを実行する権限を持っていないために、接続を拒否したい場合があります。
        # 　接続を受け入れる場合は、connect()の最後のアクションとしてaccept()を呼び出します。
        await self.accept()

    # WebSocket切断時の処理
    async def disconnect( self, close_code ):
        # クイズからの離脱
        await self.leave_quiz()

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketQuiz.send()の結果、WebSocketを介してデータがQuizConsumerに送信され、本関数で受信処理します）
    async def receive( self, text_data ):
        # 受信データをJSONデータに復元
        text_data_json = json.loads( text_data )

        # クイズへの参加時の処理
        if( 'join' == text_data_json.get( 'data_type' ) ):
            # ユーザー名をクラスメンバー変数に設定
            self.strUserName = text_data_json['username']
            # ルーム名の取得
            strRoomName = text_data_json['roomname']
            # 役割の取得
            self.strRoleType = text_data_json['role_type']
            # クイズへの参加
            await self.join_quiz( strRoomName )

        # クイズからの離脱時の処理
        elif( 'leave' == text_data_json.get( 'data_type' ) ):
            # クイズからの離脱
            await self.leave_quiz()

        # クイズの出題時の処理
        elif( 'question_submit' == text_data_json.get( 'data_type' ) ):
            # 受信処理関数の追加
            text_data_json["type"]="spread_send"
            await self.channel_layer.group_send( self.strGroupName, text_data_json )
        
        # 回答ボタンを押した時の処理
        elif( 'pushed' == text_data_json.get( 'data_type' ) ):
            # 受信処理関数の追加
            text_data_json["type"]="spread_send"
            await self.channel_layer.group_send( self.strGroupName, text_data_json )

        # 回答が提出された時の処理
        elif( 'answer_submit' == text_data_json.get( 'data_type' ) ):
            # 受信処理関数の追加
            text_data_json["type"]="spread_send"
            await self.channel_layer.group_send( self.strGroupName, text_data_json )
        
        # 正誤判定の時の処理
        elif( 'answer_bool' == text_data_json.get( 'data_type' ) ):
            # 受信処理関数の追加
            text_data_json["type"]="spread_send"
            await self.channel_layer.group_send( self.strGroupName, text_data_json )

    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def spread_send( self, data ):
        await self.send( text_data=json.dumps( data ) )

    # クイズへの参加
    async def join_quiz( self, strRoomName ):
        # 参加者数の更新、ホストの有無確認
        self.strGroupName = 'quiz_%s' % strRoomName
        room = QuizConsumer.rooms.get(self.strGroupName)
        if( None == room ):
            # ルーム管理にルーム追加
            QuizConsumer.rooms[self.strGroupName] = {'participants_count': 1, 'already_host': False}
        else:
            room['participants_count'] += 1

        # 2人目以降のホストかどうかを判別し、真の場合参加させずdata["already_host"]の値をTrueで送信。
        room = QuizConsumer.rooms.get(self.strGroupName)
        if self.strRoleType == "host":
            if room["already_host"] != True:
                room["already_host"] = True
                # グループに参加
                await self.channel_layer.group_add( self.strGroupName, self.channel_name )
            else:
                data_json = {
                'room_name': strRoomName,
                'inroom_host': "True",
                }
                await self.send( text_data=json.dumps( data_json ) )
                return
        else:
            # グループに参加
            await self.channel_layer.group_add( self.strGroupName, self.channel_name )
        # システムメッセージの作成
        strMessage = '"' + self.strUserName + '" joined. there are ' + str( QuizConsumer.rooms[self.strGroupName]['participants_count'] ) + ' participants'
        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        data = {
            'type': 'spread_send', # 受信処理関数名
            'message': strMessage, # メッセージ
            'username': USERNAME_SYSTEM, # ユーザー名
            'datetime': datetime.datetime.now().strftime( '%Y/%m/%d %H:%M:%S' ), # 現在時刻
        }
        await self.channel_layer.group_send( self.strGroupName, data )

    # クイズからの離脱
    async def leave_quiz( self ):
        if( '' == self.strGroupName ):
            return

        # グループから離脱
        await self.channel_layer.group_discard( self.strGroupName, self.channel_name )

        # 参加者数の更新、ホストの有無更新
        QuizConsumer.rooms[self.strGroupName]['participants_count'] -= 1
        if self.strRoleType == "host":
            QuizConsumer.rooms[self.strGroupName]['already_host'] = False
        # システムメッセージの作成
        strMessage = '"' + self.strUserName + '" left. there are ' + str( QuizConsumer.rooms[self.strGroupName]['participants_count'] ) + ' participants'
        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        data = {
            'type': 'spread_send', # 受信処理関数名
            'message': strMessage, # メッセージ
            'username': USERNAME_SYSTEM, # ユーザー名
            'datetime': datetime.datetime.now().strftime( '%Y/%m/%d %H:%M:%S' ), # 現在時刻
        }
        await self.channel_layer.group_send( self.strGroupName, data )

        # 参加者がゼロのときは、ルーム管理からルームの削除
        if( 0 == QuizConsumer.rooms[self.strGroupName]['participants_count'] ):
            del QuizConsumer.rooms[self.strGroupName]

        # ルーム名を空に
        self.strGroupName = ''
