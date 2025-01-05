#include <iostream>
#include "state.h"
//#include "game.h"
//#undef SDL_main
int main(int argc, char *argv[])
{

    MazeState m{10, 10};    
    std::cout <<  m.toString() << "\n" << m.get(3, 1) << ", " << m.get(1, 3);

    return 0;
}