#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

struct cell 
{
    int x,y, MED;
    std::vector<cell *> backpointers;
};


typedef std::vector<cell *> column;
typedef std::vector<cell *> row;
typedef std::vector<std::vector<cell *> > matrix;
typedef size_t index_t;

static int DEBUG_FLAG = 0;

static int inserts = 0;
static int deletes = 0;
static int substs = 0;

int min(int const&x, int const &y, int const &z)
{
    
    int result = std::min(
            std::min(
                x,
                y),
            z
    );

    if (result == x) ++deletes;
    else if (result == y) ++substs;
    else if (result == z) ++inserts;

    return result;
}

int delcost()
{
    return 1;
}

int inscost()
{
    return 1;
}

int subcost(char a, char b)
{
    return a==b ? 0 : 2;
}

std::ostream &operator<<(std::ostream&cout, matrix const &p_matrix)
{
    std::cout << "[";
    for (index_t i = 0 ; i < p_matrix.size() ; ++i)
    {
        if (i>0) std::cout << " ";
        std::cout << "[";
        for (index_t j = 0 ; j < p_matrix[0].size() ; ++j)
        {
            
            std::cout << p_matrix[i][j] -> MED;
            std::cout << "(";
            for (index_t k = 0 ; k < p_matrix[i][j]->backpointers.size() ; ++k)
            {
                cell const * const current_cell = p_matrix[i][j]->backpointers[k];
                std::cout << "[" << current_cell->x << "," << current_cell -> y << "]";
                if (k != p_matrix[i][j]->backpointers.size() - 1) std::cout << ", ";
            }
            std::cout << ")";
            if (j != p_matrix[0].size() - 1) std::cout << ", ";
        }
        std::cout << "],\n";
    }
    std::cout << "]\n";
}

void init_matrix(matrix &p_matrix,
                 size_t left_length,
                 size_t right_length)
{
    for (index_t i = 0 ; i < left_length + 1; ++i)
    {
        row t_current_row;
        for (index_t j = 0 ; j < right_length + 1; ++j)
        {
            cell *t_current_cell = new cell;
            t_current_cell -> x = i;
            t_current_cell -> y = j;
            t_current_cell -> backpointers = std::vector<cell *>();
            t_current_cell -> MED = 0; 
            t_current_row . push_back(t_current_cell);    
        }
        p_matrix.push_back(t_current_row);
    }
}

void free_matrix(matrix &p_matrix)
{
    for (index_t i = 0 ; i < p_matrix.size() ; ++i)
    {
        for (index_t j = 0 ; j < p_matrix[i].size(); ++j)
        {
            delete p_matrix[i][j];
        }
    }
}

int edit_distance(std::string const &left,
                  std::string const &right)
{
    
    matrix t_table;

    if (DEBUG_FLAG) std::cout << ">>> Initing matrix \n";

    init_matrix(
            t_table,
            left.size(),
            right.size()
    );

    if (DEBUG_FLAG) std::cout << ">>> Inited matrix \n";
    
    /*
     * This is where the DP takes place
     */

    t_table[0][0] -> MED = 0;

    if (DEBUG_FLAG)
    {
        std::cout << t_table;
        std::cout << ">>> Starting DP\n";
    }

     
    for (index_t i = 1 ; i < t_table.size() ; ++i)
    {
        t_table[i][0] -> MED = t_table[i-1][0] -> MED + delcost();
    }


    for (index_t i = 1; i < t_table[0].size() ; ++i)
    {
        t_table[0][i] -> MED = t_table[0][i-1] -> MED + inscost();
    }


    if (DEBUG_FLAG)
    {
        std::cout << t_table;
        std::cout << ">>> Doing recurrence\n"; 
    }


    for (index_t i = 1; i < t_table.size() ; ++i)
    {
        for (index_t j = 1; j < t_table[0].size() ; ++j)
        {
            int delete_value = t_table[i-1][j] -> MED + delcost();
            int subst_value = t_table[i-1][j-1] -> MED + subcost(left[i-1], right[j-1]);
            int insert_value = t_table[i][j-1] -> MED + inscost();

            if (delete_value <= subst_value && delete_value <= insert_value)
            {
                t_table[i][j] -> backpointers.push_back(t_table[i-1][j]);
            }
            if (subst_value <= delete_value && subst_value <= insert_value)
            {
                t_table[i][j] -> backpointers.push_back(t_table[i-1][j-1]);
            }
            if (insert_value <= delete_value && insert_value <= subst_value)
            {
                t_table[i][j] -> backpointers.push_back(t_table[i][j-1]);
            }

            t_table[i][j] -> MED = min(delete_value, subst_value, insert_value);
        }
    }

    if (DEBUG_FLAG)
    {
        std::cout << "Matrix : \n";
    
        std::cout << t_table;
        
        std::cout << inserts << " inserts\n" << deletes << " deletes\n" << substs << " substitutions\n were made\n";

        std::cout << ">>> Freeing matrix \n";

    }

    int result = t_table.back().back()->MED;

    free_matrix(t_table);

    if (DEBUG_FLAG) std::cout << ">>> Freed matrix \n";

    return result;
}



int main()
{
    std::string left, right;
    int t_debug_flag;
    std::cout << std::endl;
    std::cout << "Please enter the left word: ";
    std::cin >> left;
    std::cout << std::endl;
    std::cout << "Please enter the right word: ";
    std::cin >> right;
    std::cout << std::endl;
    std::cout << "Would you like debugging (YES/NO): ";
    std::cin >> t_debug_flag;
    DEBUG_FLAG = t_debug_flag;
    std::cout << std::endl;
    std::cout << "The edit distance is " << edit_distance(left, right);
    std::cout << std::endl;
    return 0;
}
