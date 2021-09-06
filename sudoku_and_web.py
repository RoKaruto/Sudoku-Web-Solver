from selenium import webdriver
from selenium.webdriver import ActionChains
import datetime as dt
import time


def print_board(bo):
    """Simple display of a 9 x 9 sudoku board, a zero value of a cell will be shown as a blank space"""
    for r in range(len(bo)):
        if r % 3 == 0 and r != 0:       # draw this line every 3 rows, but skip the first one
            print("— — — — — — — — — — — ")
        for c in range(9):
            if c % 3 == 0 and c != 0:   # draw this line every 3 columns, but skip the first one
                print("| ", end="")
            if c == 8:
                if bo[r][c] != 0:   # if c = 8, the end of the row is not reached, used to determine linebreak (end="" or not)
                    print(bo[r][c])
                else:
                    print(" ")    # the 0 value is needed for the code, but looks confusing in display, so a blank space is shown (only in unsolved puzzles)
            else:
                if bo[r][c] != 0:
                    print(str(bo[r][c]) + " ", end="")  
                else:
                    print("  ", end="")


def find_empty(bo):
    for r in range(len(bo)):
        for c in range(9):
            if bo[r][c] == 0:
                return r, c
    return None                     # no more empty fields


def valid_placement(bo, num: [int], pos: [tuple]):
    for c in range(9):
        if bo[pos[0]][c] == num and pos[1] != c:
            return False
    for r in range(len(bo)):
        if bo[r][pos[1]] == num and pos[0] != r:
            return False
    # check the 3x3 square the cell is in
    square_x = pos[1] // 3      # floor division to determine ...
    square_y = pos[0] // 3      # ... the current square
    for y in range(square_y * 3, square_y * 3 + 3):         # range from top corner of square to plus 3 down ...
        for x in range(square_x * 3, square_x * 3 + 3):     # ... and right
            if bo[y][x] == num and (y, x) != pos:
                return False
    return True


def solve(bo):
    next_empty = find_empty(bo)
    if not next_empty:      # no more empty fields -> board is solved
        return True
    else:
        r, c = next_empty
    for num in range(1, 10):
        if valid_placement(bo, num, (r, c)):
            bo[r][c] = num
            if solve(bo):       # start backtracking by recursion, if false was returned on previous recursion ...
                return True
            bo[r][c] = 0        # ... set position back to zero value in board and ...
    return False                # ... return False to check the next number in for loop of recursion


if __name__ == "__main__":

    board = [[0 for c in range(9)] for r in range(9)]     # empty board with 9 by 9 dimension containing only zeros

    chrome_driver_path = "" # put in your path to chromedriver.exe
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get("")          # PM for link, at the time of posting I was not sure, whether I can freely post a website I have no affiliation to

    time.sleep(0.2)
    driver.find_element_by_id("g4").click()     # choose "level: very hard" from website
    time.sleep(0.2)

    # read in the board
    for row in range(9):
        for col in range(9):
            cell = driver.find_element_by_id(f"vc_{row}_{col}")
            if cell.text:
                board[col][row] = int(cell.text)    # update the board, if a number is already given

    start_time = dt.datetime.now()
    solve(board)
    end_time = dt.datetime.now()

    print(f"\nSolution (found in {str(end_time-start_time).split(':')[-1][1:-2]} seconds):\n")
    print_board(board)  # show the board on console (not needed for code, can be commented out)

    # fill in the blanks :)
    for row in range(9):
        for col in range(9):
            cell_id = f"vc_{row}_{col}"
            cell = driver.find_element_by_id(cell_id)
            if not cell.text:
                move = ActionChains(driver)
                num_key = driver.find_element_by_id(f"M{str(board[col][row])}")
                time.sleep(.2)                                      # Note: the time.sleep(0.2) intervals are needed,...
                move.move_to_element(num_key).click().perform()
                time.sleep(.2)                                      # ... so the website can catch up, otherwise...
                move.move_to_element(cell).click().perform()
                time.sleep(.2)                                      # ... placement of numbers might be skipped"""
                driver.find_element_by_id(cell_id).click()

    if input("\n\nClose web driver window? (Y/n) ") == "Y":
        driver.quit()
