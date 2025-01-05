#include <iostream>
#include "state.h"
//#include "game.h"
//#undef SDL_main
#include <runner.h>
int main(int argc, char *argv[])
{
    try {
        std::shared_ptr<MazeState> m;
        Runner r = Runner(&m);
        std::cout << m->toString();

    }
    catch (std::exception e) {
        std::cout << e.what();
    }
    return 0;
}