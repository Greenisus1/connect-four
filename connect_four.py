#!/usr/bin/env python3
"""Local terminal four-in-a-row, two players or a simple computer."""
import argparse
import random
import curses
import os

ROWS,COLS=6,7

def new_board():return [['.' for _ in range(COLS)] for _ in range(ROWS)]
def moves(board):return [c for c in range(COLS) if board[0][c]=='.']
def drop(board,col,token):
    if col not in range(COLS) or token not in ('X','O'):raise ValueError('Choose column1-7.')
    for row in range(ROWS-1,-1,-1):
        if board[row][col]=='.':board[row][col]=token;return row
    raise ValueError('Column full. Choose another.')
def winner(board):
    for row in range(ROWS):
        for col in range(COLS):
            t=board[row][col]
            if t=='.':continue
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                if all(0<=row+dr*n<ROWS and 0<=col+dc*n<COLS and board[row+dr*n][col+dc*n]==t for n in range(4)):return t
    return None

def computer(board,rng=random):
    choices=moves(board)
    if not choices:raise ValueError('Board full.')
    for token in ('O','X'):
        for col in choices:
            trial=[row[:] for row in board];drop(trial,col,token)
            if winner(trial)==token:return col
    safe=[]
    for col in choices:
        trial=[row[:] for row in board];drop(trial,col,'O');danger=False
        for opp in moves(trial):
            test=[row[:] for row in trial];drop(test,opp,'X')
            if winner(test)=='X':danger=True;break
        if not danger:safe.append(col)
    choices=safe or choices
    if 3 in choices:return 3
    return rng.choice(choices)

def render(board):
    print('  1 2 3 4 5 6 7\n┌───────────────┐')
    for row in board:print('│ '+' '.join(row)+' │')
    print('└───────────────┘')

def fullscreen(screen, ai=False):
    screen.keypad(True)
    try:curses.curs_set(0)
    except curses.error:pass
    board=new_board();turn='X';selected=3;message='';done=False
    def put(y,x,text,attr=0):
        h,w=screen.getmaxyx()
        if 0<=y<h and 0<=x<w:
            try:screen.addnstr(y,x,text,max(0,w-x-1),attr)
            except curses.error:pass
    while True:
        h,w=screen.getmaxyx();screen.erase();put(0,1,'CONNECT FOUR - '+('vs computer' if ai else 'two local players'),curses.A_BOLD)
        if h<14 or w<30:put(2,1,'Resize to30x14. Esc/q quits.')
        else:
            cellw=max(3,(w-4)//7);cellh=max(1,(h-7)//6);left=max(1,(w-cellw*7)//2);top=3
            for col in range(7):put(2,left+col*cellw,str(col+1)+(' ▼' if col==selected else ''))
            for row in range(6):
                for col in range(7):
                    yy=top+row*cellh;xx=left+col*cellw
                    for offset in range(cellh):put(yy+offset,xx,'│'+' '*(cellw-1))
                    token=board[row][col]
                    label=(' '+token+' ') if token!='.' else ' · '
                    put(yy+cellh//2,max(xx+1,xx+cellw//2-1),label,curses.A_REVERSE|curses.A_BOLD if token!='.' else curses.A_DIM)
            put(min(h-4,top+6*cellh),left,'─'*(cellw*7))
            put(h-3,1,message or (turn+' turn - select a column'))
            put(h-2,1,'1-7 or arrows + Enter | Esc/q exit | R new game after finish')
        screen.refresh()
        if not done and ai and turn=='O':
            col=computer(board);drop(board,col,turn);message='Computer chose '+str(col+1)
            won=winner(board);done=bool(won or not moves(board));message=(won+' wins!' if won else 'Draw.') if done else message;turn='X';continue
        key=screen.getch()
        if key in (27,ord('q'),ord('Q')):return 0
        if done:
            if key in (ord('r'),ord('R')):board=new_board();turn='X';done=False;message=''
            continue
        if key==curses.KEY_LEFT:selected=max(0,selected-1)
        elif key==curses.KEY_RIGHT:selected=min(6,selected+1)
        elif key in (10,13) or ord('1')<=key<=ord('7'):
            if h<14 or w<30:continue
            col=key-ord('1') if ord('1')<=key<=ord('7') else selected
            try:drop(board,col,turn)
            except ValueError as exc:message=str(exc);continue
            won=winner(board);done=bool(won or not moves(board));message=won+' wins!' if won else 'Draw.' if done else '';turn='O' if turn=='X' else 'X'


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ai',action='store_true',help='human X vs simple computer O');p.add_argument('--two-player',action='store_true');p.add_argument('--plain',action='store_true',help='scrolling fallback instead of fullscreen');a=p.parse_args(argv)
    try:
        if not a.ai and not a.two_player:
            mode=input('1 Two local players  2 Computer  q Quit: ').strip().lower()
            if mode not in ('1','2'):return 0
            a.ai=mode=='2'
        if not a.plain and os.isatty(0) and os.isatty(1):return curses.wrapper(fullscreen,a.ai)
        while True:
            board=new_board();turn='X'
            print('Four in a row. Columns1-7. q quits. '+('Computer is O.' if a.ai else 'Two local players: X and O.'))
            while True:
                render(board)
                if a.ai and turn=='O':col=computer(board);print('Computer:',col+1)
                else:
                    choice=input(turn+' column: ').strip().lower()
                    if choice in ('q','quit','/quit'):return 0
                    if not choice.isascii() or not choice.isdigit() or not 1<=int(choice)<=7:print('Choose column1-7.');continue
                    col=int(choice)-1
                try:drop(board,col,turn)
                except ValueError as exc:print(exc);continue
                won=winner(board)
                if won or not moves(board):render(board);print(won+' wins!' if won else 'Draw.');break
                turn='O' if turn=='X' else 'X'
            if input('Play again? y/n: ').strip().lower()!='y':return 0
    except (EOFError,KeyboardInterrupt):return 0
    except curses.error as exc:print("Terminal stopped:",exc);return 1
if __name__=='__main__':raise SystemExit(main())
