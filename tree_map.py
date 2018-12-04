import os
from tree_rectangle import TreeRectangle, Split, inverse_split

class TreeMap:
    def __init__(self, directory):
        self.rects = {}
        self.size_map = {}
        self.calc_size_map(directory)
        self.process_dir(directory, TreeRectangle(), Split.HORIZONTAL)
        
    def calc_size_map(self, directory):
        total_size = 0
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)
            if os.path.isdir(full_path):
                self.calc_size_map(full_path)
            elif os.path.isfile(full_path):
                self.size_map[full_path] = os.path.getsize(full_path)
            else:
                print('Unknown entity type: ' + full_path)
                continue
            total_size += self.size_map[full_path]
        self.size_map[directory] = total_size
    
    def process_dir(self, directory, parent_rect, split_type):
        if self.size_map[directory] == 0:
            # no rect for empty directory
            return
        files_paths = [os.path.join(directory, filename) for filename in os.listdir(directory)]
        
        ratios = []
        for file_path in files_paths:
            ratios.append(self.size_map[file_path] / self.size_map[directory])
        
        new_rects = parent_rect.split(ratios, split_type)
        for i in range(len(files_paths)):
            file_path = files_paths[i]
            cur_rect = new_rects[i]
            if os.path.isdir(file_path):
                self.process_dir(file_path, cur_rect, inverse_split(split_type))
            elif os.path.isfile(file_path):
                self.rects[file_path] = cur_rect
            else:
                assert(False)
