import os
from tree_rectangle import TreeRectangle, Split, inverse_split

class TreeMapSquarified:
    def __init__(self, directory):
        self.rects = {}
        self.subdir_rects = {}
        self.size_map = {}
        self.calc_size_map(directory)
        self.total_size = sum([self.size_map[path] for path in self.size_map if os.path.isfile(path)])
        self.process_dir(directory, TreeRectangle())
        
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
    
    def process_dir(self, directory, rect):
        if self.size_map[directory] == 0:
            return
        
        files_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) 
                       if self.size_map[os.path.join(directory, filename)] > 0.0]
        areas = [self.size_map[file_path] / self.total_size for file_path in files_paths]
        
        # sort in descending ratio order
        areas, files_paths = zip(*sorted(zip(areas, files_paths), reverse=True))

        row_start_index = 0        
        for i in range(1, len(areas)):
            old_max_ratio = self.max_aspect_ratio(rect, areas[row_start_index: i])
            new_max_ratio = self.max_aspect_ratio(rect, areas[row_start_index: i + 1])                                     
            if old_max_ratio < new_max_ratio:
                remaining_total_areas_sum = sum(areas[row_start_index:])
                rect = self.add_row(rect, remaining_total_areas_sum, 
                                    areas[row_start_index: i],
                                    files_paths[row_start_index: i])
                row_start_index = i
        
        assert(row_start_index < len(areas))
        self.add_row(rect, sum(areas[row_start_index:]),
                    areas[row_start_index:], files_paths[row_start_index:])
        
        # recursive launch for directories
        for file_path in files_paths:
            if os.path.isdir(file_path):
                self.process_dir(file_path, self.subdir_rects[file_path])
                
    def get_split_type(self, rect):
        if rect.x_size() > rect.y_size():
            return Split.VERTICAL
        else:
            return Split.HORIZONTAL
                
    def max_aspect_ratio(self, rect, areas):
        assert(len(areas) > 0)
        width = min(rect.x_size(), rect.y_size())
        sum_area = sum(areas)
        multiplier = width**2 / sum_area**2
        return max(multiplier * areas[0], 1.0 / (multiplier * areas[-1]))
            
    def add_row(self, rect, remaining_total_areas_sum, areas, files_paths):
        external_split_type = self.get_split_type(rect)
        row_area_ratio = sum(areas) / remaining_total_areas_sum
        external_split_ratios = [row_area_ratio, 1.0 - row_area_ratio]
        external_rects = rect.split(external_split_ratios, external_split_type)
        
        internal_split_ratios = [area / sum(areas) for area in areas]
        internal_rects = external_rects[0].split(internal_split_ratios, inverse_split(external_split_type))
        for i in range(len(internal_rects)):
            if os.path.isfile(files_paths[i]):
                self.rects[files_paths[i]] = internal_rects[i] 
            elif os.path.isdir(files_paths[i]):
                self.subdir_rects[files_paths[i]] = internal_rects[i]
        return external_rects[1]
