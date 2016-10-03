/*this code is to update the database*/
var LOST_CODE = 1;
var WIN_CODE = 2;
var DRAW_CODE = 3;

var board = [0, 1, 2, 3, 4, 5, 6, 7, 8];

/*checks if the selected position is empty or not*/
var isEmpty = function(num){
	return board[num] != 'o' && board[num] != 'x';
}
/*generates a random position*/
var getRandomNum = function(){
	return Math.floor(Math.random()*8);
}
/*checks if the line contains either 'x' or 'o'*/
var  check_line = function(user, spot_a, spot_b, spot_c) {
	return board[spot_a] == user && board[spot_b] == user && board[spot_c] == user;
}
/*calls above function to check the winner*/
var winner = function(user){
	if (check_line(user, 0, 1, 2)) return true;
	else if (check_line(user, 3, 4, 5)) return true;
	else if (check_line(user, 6, 7, 8)) return true;
	else if (check_line(user, 0, 3, 6)) return true;
	else if (check_line(user, 1, 4, 7)) return true;
	else if (check_line(user, 2, 5, 8)) return true;
	else if (check_line(user, 0, 4, 8)) return true;
	else if (check_line(user, 2, 4, 6)) return true;
}
/*checks for every position from 0-8, and returns true if 
there are no spots left*/ 
var game_over = function(){
	for (var i = 0; i < 9; i++){
		if(isEmpty(i)) return false;
	}
	return true;
};

/*blocks the position if the user is going
to win in next step*/
var block = function(pos1, pos2, pos3){
	if(board[pos1] == board[pos2] && board[pos1] == 'o' && isEmpty(pos3)){
		setBoard('x', pos3);
		return true;
	}
	return false;
}

/*checks if the computer is about to win*/
var win = function(pos1, pos2, pos3){
	if(board[pos1] == board[pos2] && board[pos1] == 'x' && isEmpty(pos3)){
		setBoard('x', pos3);
		return true;
	}
	return false;
}

/*sets the position to x or o*/
var setBoard = function(ch, pos){
	board[pos] = ch;
	$('#pos_' + pos).html(ch);
}

/*
First three lines of can win check if the computer can win in next step
Next three lines check if user is winning in the next step
*/
var canwin = function(pos1, pos2, pos3){
	if (win(pos1, pos2, pos3)) return true;
	else if (win(pos1, pos3, pos2)) return true;
	else if (win(pos3, pos2, pos1)) return true;
	if (block(pos1, pos2, pos3)) return true;
	else if (block(pos1, pos3, pos2)) return true;
	else if (block(pos3, pos2, pos1)) return true;
	else return false;
};

/*checks if computer can win or lose and take the appropriate action
accordingly. If it returns false, then the computer will generate a random
position, and check if it is empty and choose a position*/
var ai = function(){
	if ( canwin(0, 1, 2)) return true;
	else if (canwin(3, 4, 5)) return true;
	else if (canwin(6, 7, 8)) return true;    
	else if (canwin(0, 3, 6)) return true;
	else if (canwin(1, 4, 7)) return true;    
	else if (canwin(2, 5, 8)) return true;    
	else if (canwin(0, 4, 8)) return true;
	else if (canwin(2, 4, 6)) return true;
	else return false;
}

var updateDataBase = function(x){
	url = "/?code=" + x;
	$.post( url, function( data ) {
	});
};

/*give the feedback to the user once the game is over
*/
var showMessage = function(code, str){
	$('#modalContent').text(str);
 	if (code == 1){ // wins
 		$('#modalTitle').text("You Won!")
 	} else if(code ==2){ // lose
 		$('#modalTitle').text("You Lost!")
 	} else if(code == 3){ // draw
 		$('#modalTitle').text("Game Draw!")
 	}
 	$('#winModal').modal('show');
 	$('.modal-btn').click(function(){
 		updateDataBase();
 		location.reload();
 	});
 };

/*this is the main*/
 $(document).ready(function(){
 	$('.table_btn').click(function(){
 		var pos = $(this).attr('id').split('_')[1];
 		if(!isEmpty(pos)){
 			alert("please choose another position");
 		} else {
 			board[pos] = 'o';
 			$(this).html('o');
 			if (winner('o')) {
 				updateDataBase(WIN_CODE);
 				showMessage(1, "Congratulations you won!!!!");
 			} else if (game_over()){
 				updateDataBase(DRAW_CODE);
 				showMessage(3, "The game was a tie!!!!");				
 			} else { 
 				if(!ai()){
 					var randNum = getRandomNum();
 					while(!isEmpty(randNum)){
 						randNum = getRandomNum();
 					}
 					setBoard('x', randNum)
 				}
 				if (winner('x')) {
 						updateDataBase(LOST_CODE);
 						showMessage(2, "You lost! Try again!!!!");
 				}
 			}
 		}
 	});
 });