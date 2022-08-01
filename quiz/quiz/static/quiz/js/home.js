// Defines
const g_elementDivJoinScreen    = document.getElementById( "div_join_screen" );
const g_elementDivHostScreen    = document.getElementById( "div_host_screen" );
const g_elementDivPlayerScreen  = document.getElementById( "div_player_screen" );
const g_elementInputUserName    = document.getElementById( "input_username" );
const g_elementInputRoomName    = document.getElementById( "input_roomname" );
const g_elementDivSelectRole    = document.getElementById( "join_screen" ).select_role;

const g_elementTextUserName     = document.getElementById( "text_username" );
const g_elementTextRoomName     = document.getElementById( "text_roomname" );

const g_elementInputMessage     = document.getElementById( "input_message" );
const g_elementQuestion         = document.getElementById( "question_area" );
const g_elementAnswer           = document.getElementById( "answer_area" );

const g_elementHostmenuAnswer   = document.getElementById( "Hostmenu_answer_describe" );
const g_elementHostmenuQuestion = document.getElementById( "Hostmenu_question_describe" );
const g_elementHostmenuCType    = document.getElementById( "Hostmenu_choisetype_describe" );

const g_elementHostmenuPName    = document.getElementById( "Hostnemu_players_name" );
const g_elementHostmenuPAnswer  = document.getElementById( "Hostnemu_players_answer_inside" );
const g_elementHostmenuPBool    = document.getElementById( "Hostmenu_players_bool" );

const g_elementQsubmitbtn       = document.getElementById( "q_submit_btn" );
const g_elementQclosebtn        = document.getElementById( "q_close_btn" );

const g_elementPModalcontent    = document.getElementById( "player_pushed" );

const self_grad_btn_T           = document.getElementById( "q_bool_true" );
const self_grad_btn_F           = document.getElementById( "q_bool_false" );

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
const g_elementClassName_PModal    = g_elementPModalcontent.className;
g_elementPModalcontent.className   = "d-none";

const default_choises_lst = [
    choises_lst[0].className,
    choises_lst[1].className,
    choises_lst[2].className,
    choises_lst[3].className,
]
for(let i=1; i<4; i++){
    choises_lst[i].className="d-none";
}

const ans_submit_btn = document.createElement( "input" );
ans_submit_btn.className = "btn btn-outline-secondary";
ans_submit_btn.type = "button";
ans_submit_btn.setAttribute('onclick', 'onclickButton_answer_submit(); return false;');
ans_submit_btn.value = "提出";

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
    g_elementHostmenuQuestion.textContent = "なし";
    while( g_elementAnswer.firstChild )
    {
        g_elementAnswer.removeChild( g_elementAnswer.firstChild );
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

// 回答ボタンが押された事をWebSocketに送信する処理
function onclickButton_answer_button()
{
    g_socket.send( JSON.stringify( { "data_type": "pushed", "pushed_player": g_elementTextUserName.value } ) );
}

// 回答のデータをWebSocketに送信する処理
function onclickButton_answer_submit()
{   
    if(g_elementAnswer.answer_choise_radio.value)
    {
        var answer = g_elementAnswer.answer_choise_radio.value;
        g_socket.send( JSON.stringify( { "data_type": "answer_submit", "pushed_player": g_elementTextUserName.value, "answer": answer, "Qtype": "num" } ) );
    }
    else
    {
        var txtarea_element = document.getElementById("answer_textarea");
        var answer = txtarea_element.value;
        g_socket.send( JSON.stringify( { "data_type": "answer_submit", "pushed_player": g_elementTextUserName.value, "answer": answer, "Qtype": "text" } ) );
    }
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

// WebSocketからデータ受信時の処理
g_socket.onmessage = ( event ) =>
{
    // テキストデータをJSONデータにデコード
    let data = JSON.parse( event.data );

    // 2人目以降のホスト参加する時は、Textデータを初期化してjoin画面に戻す。
    // 自身がまだ参加していないときは、無視。
    if(data["inroom_host"]=="True" && g_elementInputRoomName.value==data["room_name"])
    {
        g_elementDivJoinScreen.className = g_elementClassName_Join;
        g_elementDivHostScreen.className = "d-none";
        g_elementTextRoomName.value="";
        g_elementTextUserName.value="";
        return;
    }
    else if( !g_elementTextUserName.value )
    {
        return;
    }
    // 受け取ったデータが問題提出の時
    if(data["question"])
    {
        g_elementQsubmitbtn.disabled = true;
        g_elementQclosebtn.disabled = false;
        while( g_elementAnswer.firstChild )
        {
            g_elementAnswer.removeChild( g_elementAnswer.firstChild );
        }
        g_elementQuestion.textContent = data["question"];
        g_elementHostmenuQuestion.textContent = data["question"];

        var elementrow   = document.createElement( "div" );
        var elementcol_1 = document.createElement( "div" );
        var elementcol_2 = document.createElement( "div" );
        
        elementrow.className = "row";
        elementcol_1.className = "col-12 p-1 d-flex align-items-center justify-content-center";
        elementcol_2.className = "col-12 p-1 d-flex align-items-center justify-content-center";

        if(data["id"]=="0")
        {
            g_elementHostmenuCType.textContent = "記述式";
            g_elementHostmenuAnswer.textContent = "ホストの確認乞";
            var txtarea = document.createElement( "textarea" );
            txtarea.rows = "5";
            txtarea.cols = "35";
            txtarea.className = "form-control";
            txtarea.id = "answer_textarea";

            // 要素の構成
            // Answer > row > col_1 > textarea
            //              > col_2 > button

            elementcol_1.appendChild( txtarea );
            elementcol_2.appendChild( ans_submit_btn );
            elementrow.appendChild( elementcol_1 );
            elementrow.appendChild( elementcol_2 );
            g_elementAnswer.appendChild( elementrow );
        }
        else
        {
            g_elementHostmenuCType.textContent = String(Number(data["id"])+1)+"択問題";
            g_elementHostmenuAnswer.textContent = data["answer"];
            for(let i=0; i<Number(data["id"])+1; i++)
            {
                var num = "choise"+String(i+1);
                var elementdiv   = document.createElement( "div" );
                var elementradio = document.createElement( "input" );
                var text         = document.createTextNode( data[num] );

                elementdiv.className = "form-check form-check-inline";

                elementradio.className = "form-check-input";
                elementradio.type = "radio";
                elementradio.name = "answer_choise_radio";
                elementradio.value = String(i+1);

                // 要素の構成
                // Answer > row > col_1 > radio & text
                //              > col_2 > button

                elementdiv.appendChild( elementradio );
                elementdiv.appendChild( text );
                elementcol_1.appendChild( elementdiv );
                elementcol_2.appendChild( ans_submit_btn );
                elementrow.appendChild( elementcol_1 );
                elementrow.appendChild( elementcol_2 );
                g_elementAnswer.appendChild( elementrow );
            }
        }
    }
    // 受け取ったデータが回答ボタンを押した通知時の処理
    else if(data["pushed_player"] && !data["Qtype"])
    {
        // プレイヤー画面操作
        if(g_elementDivHostScreen.className==="d-none")
        {
            $("#pushed_modal").modal("show");
            // 回答者
            if(g_elementTextUserName.value===data["pushed_player"])
            {
                g_elementPModalcontent.textContent = "";
                g_elementPModalcontent.className = "d-none";
                g_elementAnswer.className = "";
            }
            // それ以外
            else
            {
                g_elementPModalcontent.textContent = data["pushed_player"]+"が入力中です。";
                g_elementPModalcontent.className = g_elementClassName_PModal;
                g_elementAnswer.className = "d-none";
            }
        }
        // ホスト画面操作
        else
        {
            g_elementHostmenuPName.textContent = data["pushed_player"];
            g_elementHostmenuPAnswer.textContent = "回答中";
            g_elementHostmenuPBool.textContent = "不明";
        }
    }
    // 受け取ったデータが回答の提出の時
    else if(data["Qtype"])
    {
        // 正誤判定のデータを送るのはホストのみ
        if(g_elementDivHostScreen.className!=="d-none")
        {
            g_elementHostmenuPAnswer.textContent = data["answer"];
            if(data["Qtype"]==="text")
            {
                self_grad_btn_T.disabled = "false";
                self_grad_btn_F.disabled = "false";
            }
            else
            {
                if(data["answer"]===g_elementHostmenuAnswer.textContent)
                {
                    g_socket.send( JSON.stringify( { "data_type": "answer_bool", "bool": "true", "player_name": data["pushed_player"], "answer": data["answer"] } ) );
                }
                else
                {
                    g_socket.send( JSON.stringify( { "data_type": "answer_bool", "bool": "false", "player_name": data["pushed_player"], "answer": data["answer"] } ) );
                }
            }
        }
    }
    // 受け取ったデータが正誤判定を全体送信する時
    else if(data["bool"])
    {
        if(data["bool"]==="true")
        {
            g_elementHostmenuPBool.textContent = "正解";
            $("#pushed_modal").modal("hide");
        }
        else
        {
            g_elementHostmenuPBool.textContent = "不正解";
            $("#pushed_modal").modal("hide");
        }
    }
};

// WebSocketクローズ時の処理
g_socket.onclose = ( event ) =>
{
    // ウェブページを閉じたとき以外のWebSocketクローズは想定外
    console.error( "Unexpected : Quiz socket closed." );
};