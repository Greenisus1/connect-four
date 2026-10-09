# Four-in-a-row (name pending)

Terminal dropping-disc game. Two local players or simple computer opponent, chosen when opening. Connect four horizontally, vertically or diagonally in a7-column,6-row board. ASCII X/O pieces in Unicode frame, no color dependence. Offline Python3 standard library, no AI service, network, saved history or packages.

    python3 connect_four.py
    python3 connect_four.py --ai
    python3 connect_four.py --two-player

Fullscreen by default in an interactive terminal. Board scales to terminal size; arrows+Enter or1-7 drop a piece, Esc/q exits, R starts a new board after win/draw. --plain retains scrolling mode with y replay. Tiny terminal asks to resize rather than crashing. Full/invalid columns preserve current turn. Computer checks immediate win, blocks immediate loss, avoids obvious next-turn losses when possible, then prefers center or random valid column. It is a simple opponent, not solved-game strength. Independent four-in-a-row implementation, not affiliated with the toy maker.

Games in the normal Store, not beta. Install syntax-checks only. Seven unit tests cover gravity/full column, all win directions, no wrap, computer win/block and no mutation, end-game/replay quit. Real Linux PTY render/quit inspected. Raspberry Pi hardware untested.
