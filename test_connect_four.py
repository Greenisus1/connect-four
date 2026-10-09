import unittest
from unittest.mock import patch
import connect_four as a
class Tests(unittest.TestCase):
 def test_gravity_and_full(self):
  b=a.new_board()
  for n in range(6):self.assertEqual(a.drop(b,0,'X'),5-n)
  with self.assertRaises(ValueError):a.drop(b,0,'O')
 def test_all_win_directions(self):
  for r,c,dr,dc in [(5,0,0,1),(0,0,1,0),(0,0,1,1),(0,6,1,-1)]:
   b=a.new_board()
   for i in range(4):b[r+dr*i][c+dc*i]='X'
   self.assertEqual(a.winner(b),'X')
 def test_no_wrap(self):
  b=a.new_board();b[5][6]=b[4][0]=b[4][1]=b[4][2]='X';self.assertIsNone(a.winner(b))
 def test_ai_win_block(self):
  for token in ('O','X'):
   b=a.new_board()
   for c in range(3):a.drop(b,c,token)
   self.assertEqual(a.computer(b),3)
 def test_ai_no_mutation(self):
  b=a.new_board();old=[r[:] for r in b];self.assertEqual(a.computer(b),3);self.assertEqual(b,old)
 def test_quit(self):
  with patch('builtins.input',return_value='q'),patch('builtins.print'):self.assertEqual(a.main(['--two-player']),0)
 def test_win_and_stop(self):
  with patch('builtins.input',side_effect=['1','2','1','2','1','2','1','n']),patch('builtins.print') as out:
   self.assertEqual(a.main(['--two-player']),0);self.assertIn(('X wins!',),[c.args for c in out.call_args_list])
