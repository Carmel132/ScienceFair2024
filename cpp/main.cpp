// #include <iostream>
// #include "state.h"
#include "game.h"
// #undef SDL_main
// #include <memory>
// #include <runner.h>
// #include "render.h"
#include <iostream>
int main(int argc, char *argv[]) {
  std::cout << "Hello";
  auto g = new Game();
  g->run();
  std::cout << "Done";

  return 0;
}
