#include <iostream>
//#include "state.h"
//#include "game.h"
//#undef SDL_main
#include <runner.h>
int main(int argc, char *argv[])
{

    SetCell c{"loc=(2, 1), old=1, new=0, TYPE=ActionTypes.SETCEL"};
    std::cout << c.loc.first << " " << c.loc.second << " " << c.old;
    return 0;
}