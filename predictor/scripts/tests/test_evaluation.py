import unittest
import evaluation

 
class TestEvaluation(unittest.TestCase):
     def test_check_each_result(self):
          # success pattern
          ## 1
          success_dict_1 = [{'1': [1,1]}, {'2': [1,1]}, {'3': [2,2]}, {'4': [2,2]}, {'5': [1,1]}, {'6': [1,1]}, {'7': [1,1]}, {'8': [2,2]}, {'9': [2,2]}, {'10': [1,1]}, {'11': [1,1]}, {'12': [1,1]}, {'13': [2,2]}]
          ## 2
          success_dict_2 = [{'1': [1,1]}, {'2': [1,1]}, {'3': [2,2]}, {'4': [2,2]}, {'5': [1,1]}, {'6': [1,1]}, {'7': [1,1]}, {'8': [2,2]}, {'9': [2,0]}, {'10': [1,1]}, {'11': [1,1]}, {'12': [1,1]}, {'13': [2,2]}]
          ## 3
          success_dict_3 = [{'1': [1,1]}, {'2': [1,1]}, {'3': [2,2]}, {'4': [2,2]}, {'5': [1,0]}, {'6': [1,1]}, {'7': [1,1]}, {'8': [2,2]}, {'9': [2,2]}, {'10': [1,1]}, {'11': [1,1]}, {'12': [1,2]}, {'13': [2,2]}]
          # failed pattern
          failed_dict = [{'1': [1,1]}, {'2': [1,1]}, {'3': [2,2]}, {'4': [2,2]}, {'5': [1,1]}, {'6': [1,1]}, {'7': [1,2]}, {'8': [2,2]}, {'9': [2,0]}, {'10': [1,1]}, {'11': [1,1]}, {'12': [1,0]}, {'13': [2,2]}]

          # 1st check
          flag1 = evaluation.check_each_round(success_dict_1)
          # 2nd check
          flag2 = evaluation.check_each_round(success_dict_2)
          # 3rd check
          flag3 = evaluation.check_each_round(success_dict_3)
          # failed check
          failed_flag = evaluation.check_each_round(failed_dict)
          
          self.assertTrue(flag1 == 1 and flag2 == 2 and flag3 == 3 and failed_flag == 0)
          
if __name__ == "__main__":
    unittest.main()
