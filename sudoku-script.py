class sudoku_board(object):
    def __init___(self, cell_names, cell_dict):
        self.cell_names = cell_names
        self.empty_domains = False
        if cell_dict == None:
            self.cell_dict = {}
            for name in cell_names:
                self.cell_dict[name] = range(1,10)
        else:
            self.cell_dict = cell_dict
    
    def has_empty_domains(self):
        return self.empty_domains
    
    def elim_singles(self):
        cells = self.get_single_val_cells()
        while cells != None:
            self.mark_singles(cells)
            if self.has_empty_domains():
                break
            cells = self.get_single_val_cells()
    
    def get_single_val_cells(self):
        single_vals = []
        for cell in self.cell_dict:
            if cell.is_marked() == False and len(self.cell_dict[cell]) == 1:
                single_vals.append(cell)
        return single_vals
    
    def mark_singles(self, cells):
        for cell in cells:
            val = self.cell_dict[cell][0]
            self.mark(cell, val)
    
    def mark(self, cell, val):
        self.cell_dict[cell] = val
        self.update_peers(cell)
        
    def update_peers(self, cell):
        val = self.cell_dict[cell]
        peers = self.get_peers(cell)
        for peer in peers:
            if val in self.cell_dict[peer]:
                self.cell_dict[peer].remove(val)
            if self.cell_dict[peer] == []:
                self.empty_domains = True
    
    # TODO: get_row, get_col, get_unit
    
    def get_peers(self, cell):
        row = self.get_row(cell) - [cell]
        col = self.get_col(cell) - [cell]
        unit = self.get_unit(cell) - [cell]
        return (row + col + unit).remove_copies()
    
    def clone(self):
        return sudoku_board(self.cell_names, self.cell_dict)
    
    def get_best_cell(self):
        cells = self.get_cells_that_are('marked')
        best = cells [0]
        for cell in cells:
            if len( self.cell_dict[cell] ) < len( self.cell_dict[best] ):
                best = cell
        return best
    
    def is_solved(self):
        for val in self.cell_dict.values():
            if type(val) == list:
                return False
        return True
    
    def get_cells_that_are(self, cell_type):
        cell_list = []
        for cell in self.cell_dict:
            if type(self.cell_dict[cell]) == list:
                cell_list.append(cell)
        if cell_type == 'marked':
            return [cell for cell in self.cell_dict.keys() if cell not in cell_list]
        return cell_list
    
    def add_val_to_cells(self, cells, val):
        for cell in cells:
            self.cell_dict[cell].append(val)
            self.cell_dict[cell].sort()
    
    def get_peers_with_val(self, cell, val):
        all_peers = self.get_peers(cell)
        unmarked_peers = [cell for cell in all_peers if type(self.cell_dict[cell]) == list]
        peers_with_val = [cell for cell in unmarked_peers if val in self.cell_dict[cell]]
        return peers_with_val

def solve(sudoku):
    if sudoku.is_solved():
        return sudoku
    sudoku.elim_singles()
    if sudoku.has_empty_domains():
        return False
    best_cell = sudoku.get_best_cell()
    for val in sudoku.cell_dict[best_cell][:]:
        peers_with_val = sudoku.get_peers_with_val(best_cell, val) + [best_cell]
        sudoku.mark(best_cell, val)
        if sudoku.has_empty_domains():
            sudoku.add_val_to_cells(peers_with_val, val)
        else:
            sudoku_clone = sudoku.clone()
            attempt = solve(sudoku_clone)
            if attempt != False:
                return attempt
            sudoku.add_val_to_cells(peers_with_val, val)
    return False
    