#include "game.h"

void Game::OnKeyPress(SDL_Keysym key) {
  if (key.sym == SDLK_RIGHT) {
    next();
  } else if (key.sym == SDLK_LEFT) {
    back();
  }
}

void Game::back() {
  runner.back();
  gameRenderer.GenerateCellRects(*maze, screenDimensions);
}

void Game::next() {
  runner.next();
  gameRenderer.GenerateCellRects(*maze, screenDimensions);
}

void Game::GameInit() {
  screenDimensions.cellWidth = 1 + 2 * maze->getWidth();
  screenDimensions.cellHeight = 1 + 2 * maze->getHeight();
  OnScreenUpdate();
}

void Game::OnScreenUpdate() {
  SDL_GetWindowSize(gameRenderer.window, &screenDimensions.pxWidth,
                    &screenDimensions.pxHeight);

  std::cerr << screenDimensions.pxWidth << ", " << screenDimensions.pxHeight
            << "\n";
  gameRenderer.GenerateCellPoints(screenDimensions);
  gameRenderer.GenerateCellRects(*maze, screenDimensions);
}

void Game::run() {

  if (!InitSDL()) {
    SDL_Log("Failed to initalize!\n");
    return;
  }
  std::cerr << "\n" << maze->toString() << "\n";
  GameInit();

  /*for (const std::vector<Point>& r : cellPoints) {
      for (const Point& p : r){
          std::cout << p.x << ", " << p.y << "\n";
      }
  }*/
  bool quit = false;
  SDL_Event e;
  while (!quit) {
    // Event
    while (SDL_PollEvent(&e) != 0) {
      if (e.type == SDL_QUIT) {
        quit = true;
      } else if (e.type == SDL_KEYDOWN) {
        OnKeyPress(e.key.keysym);
      }
    }

    // runner.next();
    //  Render

    gameRenderer.render();
  }

  // Shutdown
  gameRenderer.shutDownSDL();
}

int Game::InitSDL() { return gameRenderer.initSDL(); }
