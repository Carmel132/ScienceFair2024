#include <iostream>
#include "state.h"
//#include "game.h"
//#undef SDL_main
#include <runner.h>
int main(int argc, char *argv[])
{
    std::shared_ptr<MazeState> m;
    Runner r = Runner(&m);
    r.next();
    r.next();
    r.next();

    std::cout << m->toString();

    return 0;
}