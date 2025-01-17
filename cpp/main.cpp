//#include <iostream>
//#include "state.h"
#include "game.h"
//#undef SDL_main
//#include <memory>
#include <runner.h>
//#include "render.h"
int main(int argc, char *argv[])
{
    auto g = new Game();
    g->run();
    return 0;
}
