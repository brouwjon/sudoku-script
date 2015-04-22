class sudoku_board(object):
#    def __init___(self, cell_dict):
    def __init__(self, number, cell_dict):
        self.cell_names = cross('ABCDEFGHI', '123456789')
        self.empty_domains = False
        if cell_dict == None:
            self.cell_dict = {}
            for name in self.cell_names:
                self.cell_dict[name] = range(1,10)
        else:
            self.cell_dict = cell_dict
    
    def clone(self):
        return sudoku_board(self.cell_names, self.cell_dict)
    
    def is_solved(self):
        for val in self.cell_dict.values():
            if type(val) == list:
                return False
        return True
    
    def has_empty_domains(self):
        return self.empty_domains
    
    def get_num_marked(self):
        num = 0
        for cell in self.cell_dict.values():
            if type(cell) == int:
                num += 1
        return num
    
    def process_string(self, string):
        row_characters, column_numbers = 'ABCDEFGHI', '123456789'
        column_index, row_index = 0, 0

        for index_in_string in range(len(string)):
            if column_index == 9:
                column_index = 0
                row_index += 1
            
            row = row_characters[row_index]
            column = column_numbers[column_index]
            cell = row + column
            try:
                cell_value = int(string[index_in_string])
            except:
                cell_value = None

            if cell_value is not None:
                self.mark(cell, cell_value)
            column_index += 1
        
    def display(self):
        rows = 'ABCDEFGHI'
        cols = '123456789'
        print ''
        for i, r in enumerate(rows):
            if i in [3, 6]:
                print '------+-------+------'
            for j, c in enumerate(cols):
                if j in [3, 6]:
                    print '|',
                if type(self.cell_dict[r + c]) == list:
                    print '.', 
                elif type(self.cell_dict[r + c]) == int:
                    print self.cell_dict[r + c],
            print
        print ''
    
    
    ## GET CELLS ##    
    
    def get_row(self, cell):
        row = cell[0]
        return cross(row, '123456789')
    
    def get_col(self, cell):
        col = cell[1]
        return cross('ABCDEFGHI', col)
        
    def get_unit(self, cell):
        units = [cross(row, col) for row in ('ABC','DEF','GHI') for col in ('123','456','789')]
        for unit in units:
            if cell in unit:
                return unit
    
    def get_best_cell(self):
        cells = self.get_cells_that_are('unmarked')
        best = cells [0]
        for cell in cells:
            if len( self.cell_dict[cell] ) < len( self.cell_dict[best] ):
                best = cell
        return best
    
    def get_cells_that_are(self, cell_type):
        cell_list = []
        for cell in self.cell_dict:
            if type(self.cell_dict[cell]) == list:
                cell_list.append(cell)
        if cell_type == 'marked':
            return [cell for cell in self.cell_dict.keys() if cell not in cell_list]
        return cell_list
    
    
    ## MARK CELL / UPDATE PEER ##
    
    def mark(self, cell, val):
        self.cell_dict[cell] = val
        self.update_peers(cell)
        
    def update_peers(self, cell):
        val = self.cell_dict[cell]
        all_peers = self.get_peers(cell)
        unmarked_peers = [cell for cell in all_peers if type(self.cell_dict[cell]) == list]
        for peer in unmarked_peers:
            if val in self.cell_dict[peer]:
                self.cell_dict[peer].remove(val)
            if self.cell_dict[peer] == []:
                self.empty_domains = True
    
    def get_peers(self, cell):
        row = self.get_row(cell)
        col = self.get_col(cell)
        unit = self.get_unit(cell)
        peers = set(row + col + unit)
        peers.remove(cell)
        return peers
    
    def get_peers_with_val(self, cell, val):
        all_peers = self.get_peers(cell)
        unmarked_peers = [cell for cell in all_peers if type(self.cell_dict[cell]) == list]
        peers_with_val = [cell for cell in unmarked_peers if val in self.cell_dict[cell]]
        return peers_with_val
    
    def add_val_to_cells(self, cells, val):
        for cell in cells:
            self.cell_dict[cell].append(val)
            self.cell_dict[cell].sort()
        
    
    
    ## ELIMINATE SINGLES AND UPDATE ##
    
    def elim_singles(self):
        cells = self.get_single_val_cells()
        while cells != []:
            self.mark_singles(cells)
            if self.has_empty_domains():
                break
            cells = self.get_single_val_cells()
    
    def get_single_val_cells(self):
        single_vals = []
        for cell in self.cell_dict:
            if type(self.cell_dict[cell]) == list and len(self.cell_dict[cell]) == 1:
                single_vals.append(cell)
        return single_vals
    
    def mark_singles(self, cells):
        for cell in cells:
            try:
                val = self.cell_dict[cell][0]
                self.mark(cell, val)
            except:
                pass

#####

def solve(sudoku):
    # TODO: sudoku goes several recursive layers until num_bfore != num_after
    # ... ... (sudoku instance is modified by calling solve(sudoku_clone) )
    # ... When that happens, some of best_cell's peers are actually marked
    #   ... ( i.e. add_val_to_cells(peers) throws error-- (append to int)
    print "recursion"
    if sudoku.is_solved():
        return sudoku
    sudoku.elim_singles()
    if sudoku.has_empty_domains():
        return False
    best_cell = sudoku.get_best_cell()
    for val in sudoku.cell_dict[best_cell][:]:
        peers_with_val = sudoku.get_peers_with_val(best_cell, val)
        sudoku.mark(best_cell, val)
        if sudoku.has_empty_domains():
            sudoku.add_val_to_cells(peers_with_val, val)
        else:
            num_before = sudoku.get_num_marked()
            sudoku_clone = sudoku.clone()
            attempt = solve(sudoku_clone)
            assert num_before == sudoku.get_num_marked()
            if attempt != False:
                return attempt
            sudoku.add_val_to_cells(peers_with_val, val)
    return False

def cross(A, B):
    return [a+b for a in A for b in B]

######


######

string = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
#
board = sudoku_board(5, cell_dict = None)
board.process_string(string)
board.display()

solved = solve(board)
#solved.display()