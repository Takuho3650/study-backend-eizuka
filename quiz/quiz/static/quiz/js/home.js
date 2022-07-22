// Defines
const g_elementDivJoinScreen   = document.getElementById( "div_join_screen" );
const g_elementDivHostScreen   = document.getElementById( "div_host_screen" );
const g_elementDivPlayerScreen = document.getElementById( "div_player_screen" );
const g_elementInputUserName   = document.getElementById( "input_username" );
const g_elementInputRoomName   = document.getElementById( "input_roomname" );
const g_elementDivSelectRole   = document.getElementById( "join_screen" ).select_role;

const g_elementTextUserName    = document.getElementById( "text_username" );
const g_elementTextRoomName    = document.getElementById( "text_roomname" );

const g_elementInputMessage    = document.getElementById( "input_message" );
const g_elementQuestion        = document.getElementById( "question_area" );
const g_elementAnswer          = document.getElementById( "answer_area" );
const g_elementChoises         = document.getElementById( "choises_area" );

const choises_lst = [
    document.getElementById("div_choises1"),
    document.getElementById("div_choises2"),
    document.getElementById("div_choises3"),
    document.getElementById("div_choises4"),
]

// class値のコピーと初期値設定
const g_elementClassName_Join      = g_elementDivJoinScreen.className;
const g_elementClassName_Host      = g_elementDivHostScreen.className;
g_elementDivHostScreen.className   = "d-none";
const g_elementClassName_Player    = g_elementDivPlayerScreen.className;
g_elementDivPlayerScreen.className = "d-none";
const g_elementClassName_Answer    = g_elementAnswer.className;
g_elementAnswer.className          = "d-none";

const default_choises_lst = [
    choises_lst[0].className,
    choises_lst[1].className,
    choises_lst[2].className,
    choises_lst[3].className,
]
for(let i=1; i<4; i++){
    choises_lst[i].className="d-none";
}

// WebSocketオブジェクト
let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const g_socket = new WebSocket( ws_scheme + "://" + window.location.host + "/ws/quiz/" );

// 「Join」ボタンを押すと呼ばれる関数
function onsubmitButton_JoinQuiz()
{
    // 不正な入出のブロック、ユーザー名と役割分け
    let strInputUserName = g_elementInputUserName.value;
    let role_type = g_elementDivSelectRole.value;
    // ルーム名
    let strInputRoomName = g_elementInputRoomName.value;
    g_elementTextRoomName.value = strInputRoomName;
    if( !strInputUserName || role_type==="" ||  strInputRoomName=="")
    {
        return;
    }
    g_elementTextUserName.value = strInputUserName;

    // サーバーに"join"を送信
    g_socket.send( JSON.stringify( { "data_type": "join", "username": strInputUserName, "roomname": strInputRoomName, "role_type": role_type } ) );

    // ロールごとの画面の切り替え
    g_elementDivJoinScreen.className = "d-none";  // 参加画面の非表示
    if(role_type=="player"){
        g_elementDivPlayerScreen.className = g_elementClassName_Player;  // プレイヤー
    }
    else{
        g_elementDivHostScreen.className = g_elementClassName_Host;  // ホスト
    }
}

// 「Leave Quiz.」ボタンを押すと呼ばれる関数
function onclickButton_LeaveQuiz()
{
    // 問題のクリア
    g_elementQuestion.textContent = "なし";
    while( g_elementChoises.firstChild )
    {
        g_elementChoises.removeChild( g_elementChoises.firstChild );
    }

    // ユーザー名
    g_elementTextUserName.value = "";

    // サーバーに"leave"を送信
    g_socket.send( JSON.stringify( { "data_type": "leave" } ) );

    // 画面の切り替え
    g_elementDivHostScreen.className   = "d-none";  // クイズ画面の非表示
    g_elementDivPlayerScreen.className = "d-none";  // クイズ画面の非表示
    g_elementDivJoinScreen.className   = g_elementClassName_Join;  // 参加画面の表示
}

// 問題形式選択の処理
// 0, 記述式
// 1~3, n+1択問題
function editQuestion()
{
    // 選択した形式値の受け取りと画面切り替え
    let id = Number(document.getElementById("Question_choises").value);
    
    for(let i=0; i<4; i++){
        if(i==id){
            choises_lst[i].className = default_choises_lst[i];
        }
        else{
            choises_lst[i].className = "d-none";
        }
    }
}

// 「Send」ボタンを押したときの処理
function onsubmitButton_Send()
{
    // 送信用テキストHTML要素からメッセージ文字列の取得
    let strMessage = g_elementInputMessage.value;
    if( !strMessage )
    {
        return;
    }

    // WebSocketを通したメッセージの送信
    g_socket.send( JSON.stringify( { "message": strMessage } ) );

    // 送信用テキストHTML要素の中身のクリア
    g_elementInputMessage.value = "";
}

// クイズ問題をWebSocketに送信する処理
function onsubmitButton_SubmitQuiz()
{
    let id = Number(document.getElementById("Question_choises").value);
    if(id==0)
    {
        let question=document.getElementById("input_question_describe1").value;
        g_socket.send( JSON.stringify( { "data_type": "question_submit", "id": String(id), "question": question } ) );
    }
    if(id==1)
    {
        let question = document.getElementById("input_question_describe2").value;
        let choise1 = document.getElementById("input_question_choises2_option1").value;
        let choise2 = document.getElementById("input_question_choises2_option2").value;
        let answer = document.getElementById("choises2_screen").answer_choises2.value;

        g_socket.send( JSON.stringify( { "data_type": "question_submit", "id": String(id), "question": question, "choise1": choise1, "choise2": choise2, "answer": answer } ) );
    }
    if(id==2)
    {
        let question = document.getElementById("input_question_describe3").value;
        let choise1 = document.getElementById("input_question_choises3_option1").value;
        let choise2 = document.getElementById("input_question_choises3_option2").value;
        let choise3 = document.getElementById("input_question_choises3_option3").value;
        let answer = document.getElementById("choises3_screen").answer_choises3.value;

        g_socket.send( JSON.stringify( { "data_type": "question_submit", "id": String(id), "question": question, "choise1": choise1, "choise2": choise2, "choise3": choise3, "answer": answer } ) );
    }
    if(id==3)
    {
        let question = document.getElementById("input_question_describe4").value;
        let choise1 = document.getElementById("input_question_choises4_option1").value;
        let choise2 = document.getElementById("input_question_choises4_option2").value;
        let choise3 = document.getElementById("input_question_choises4_option3").value;
        let choise4 = document.getElementById("input_question_choises4_option4").value;
        let answer = document.getElementById("choises4_screen").answer_choises4.value;

        g_socket.send( JSON.stringify( { "data_type": "question_submit", "id": String(id), "question": question, "choise1": choise1, "choise2": choise2, "choise3": choise3, "choise4": choise4, "answer": answer } ) );
    }
}

// WebSocketからメッセージ受信時の処理
g_socket.onmessage = ( event ) =>
{
    // テキストデータをJSONデータにデコード
    let data = JSON.parse( event.data );

    // 自身がまだ参加していないときは、無視。
    // 2人目以降のホスト参加する時join画面に戻す。
    if(data["inroom_host"]=="True" && g_elementInputRoomName.value==data["room_name"])
    {
        g_elementDivJoinScreen.className = g_elementClassName_Join;
        g_elementDivHostScreen.className = "d-none";
        return;
    }
    if( !g_elementTextUserName.value )
    {
        return;
    }
    // 受け取ったデータが問題の提出の時
    if(data["question"])
    {
        while( g_elementChoises.firstChild )
        {
            g_elementChoises.removeChild( g_elementChoises.firstChild );
        }
        g_elementQuestion.textContent = data["question"];
        if(data["id"]=="0")
        {
            g_elementAnswer.className = g_elementClassName_Answer;
        }
        else
        {
            g_elementAnswer.className = "d-none";
            for(let i=0; i<Number(data["id"])+1; i++)
            {
                var elementradio = document.createElement( "input" );
                var num = "choise"+String(i+1);
                elementradio.type = "radio";
                elementradio.name = "answer_choise_radio";
                elementradio.value = data[num];
                var text = document.createTextNode(data[num]);
                var br = document.createElement("br");
                g_elementChoises.appendChild( elementradio );
                g_elementChoises.appendChild( text );
                g_elementChoises.appendChild( br );
            }
        }
    }
};

// WebSocketクローズ時の処理
g_socket.onclose = ( event ) =>
{
    // ウェブページを閉じたとき以外のWebSocketクローズは想定外
    console.error( "Unexpected : Quiz socket closed." );
};