# rect = (x_left, y_down, x_right, y_upper)
#
#             x_left             x_right 
#
# y_down      |------------------|
#             |                  |
#             |                  |
#             |                  |
# y_upper     |------------------|

import copy
from enum import Enum

class Split(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

def inverse_split(split):
    if split == Split.HORIZONTAL:
        return Split.VERTICAL
    elif split == Split.VERTICAL:
        return Split.HORIZONTAL
    else:
        assert(False)

class TreeRectangle:
    def __init__(self, rect=(0.0, 0.0, 1.0, 1.0)):
        assert(len(rect) == 4)
        self.x_left = rect[0]
        self.y_down = rect[1]
        self.x_right = rect[2]
        self.y_upper = rect[3]
        assert(self.x_size() > 0 and self.y_size() > 0)
        for coord in rect:
            assert(self.check_component(coord))
            
    def get_start_point(self):
        return (self.x_left, self.y_down)
            
    def x_size(self):
        return self.x_right - self.x_left
    
    def y_size(self):
        return self.y_upper - self.y_down
 
    def __repr__(self):
         return '({}, {}, {}, {})'.format(self.x_left, self.y_down, self.x_right, self.y_upper)

    def __str__(self):
         return '({}, {}, {}, {})'.format(self.x_left, self.y_down, self.x_right, self.y_upper)
        
    def create_sub_rectangle(self, ratio, shift, split_type):
        sub_rectangle = copy.copy(self)
        if split_type == Split.HORIZONTAL:
            sub_size = ratio * (self.y_upper - self.y_down)
            sub_rectangle.y_down += shift
            sub_rectangle.y_upper = sub_rectangle.y_down + sub_size
        elif split_type == Split.VERTICAL:
            sub_size = ratio * (self.x_right - self.x_left)
            sub_rectangle.x_left += shift
            sub_rectangle.x_right = sub_rectangle.x_left + sub_size
        else:    
            assert(False)
        return sub_rectangle
        
    def check_component(self, coord):
        return 0.0 <= coord <= 1.0
    
    def check_ratios(self, ratios):
        sum_ratios = sum(ratios)
        if not (abs(sum_ratios - 1.0) < 1e-10):
            print(sum_ratios)
            assert(False)
    
    def split(self, ratios, split_type):
        self.check_ratios(ratios)
        
        splitted_rectangles = []
        cummulative_shift = 0.0
        for ratio in ratios:
            sub_rect = self.create_sub_rectangle(ratio, cummulative_shift, split_type)
            splitted_rectangles.append(sub_rect)
            if split_type == Split.HORIZONTAL:
                cummulative_shift += splitted_rectangles[-1].y_size() 
            elif split_type == Split.VERTICAL:
                cummulative_shift += splitted_rectangles[-1].x_size()
        return splitted_rectangles
