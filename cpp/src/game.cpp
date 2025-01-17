#include "game.h"

void Game::GenerateCellPoints() {
        int dx = std::min((screenDimensions.pxHeight-screenDimensions.padding) / screenDimensions.cellHeight, (screenDimensions.pxWidth - screenDimensions.padding) / screenDimensions.cellWidth);
        Point centerOffset = Point((screenDimensions.pxWidth - screenDimensions.cellWidth * dx) / 2, (screenDimensions.pxHeight - screenDimensions.cellHeight * dx) / 2);
        std::cout << "dx: " << dx << ", cox: " << centerOffset.x << ", coy: " << centerOffset.y << "\n";
        for (int x = 0; x < screenDimensions.cellWidth; ++x) {
            std::vector<Point> v;
            for (int y = 0; y < screenDimensions.cellHeight; ++y) {
                v.push_back(Point(centerOffset.x + x * dx, centerOffset.y + y * dx));
            }
            cellPoints.push_back(v);
        }
        screenDimensions.cellSize = dx;
}

void Game::GameInit() {
    screenDimensions.cellWidth = 1+2*maze->getWidth();
    screenDimensions.cellHeight = 1+2*maze->getHeight();
    OnScreenUpdate();
}

void Game::OnScreenUpdate() {
    SDL_GetWindowSize(window, &screenDimensions.pxWidth, &screenDimensions.pxHeight);

    std::cerr << screenDimensions.pxWidth << ", " << screenDimensions.pxHeight << "\n";
    GenerateCellPoints();
}

void Game::run() {

    if(!InitSDL())
    {
        SDL_Log("Failed to initalize!\n");
        return;
    }
    //runner.end();
    std::cerr << "\n" << maze->toString() << "\n";
    GameInit();

    for (const std::vector<Point>& r : cellPoints) {
        for (const Point& p : r){
            std::cout << p.x << ", " << p.y << "\n";
        }
    }
    runner.end();
    bool quit = false;
    SDL_Event e;
    while(!quit)
    {
        // Event
        while(SDL_PollEvent(&e) != 0)
        {
            if(e.type == SDL_QUIT)
            {
                quit = true;
            }

        }

        //runner.next();
        // Render
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0xff);
        SDL_RenderClear(renderer);

        SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xff);

        RenderCells(renderer, cellPoints, *maze, screenDimensions);


        SDL_RenderPresent(renderer);
    }


    // Shutdown
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
	renderer = NULL;
    window =  NULL;

    SDL_Quit();
}

int Game::InitSDL() {

    int Success = 1;

    if(SDL_Init(SDL_INIT_VIDEO) != 0)
    {
        SDL_Log("Failed to initialize SDL! SDL_GetError: %s\n", SDL_GetError());
        Success = 0;
    }
    else
    {
        window = SDL_CreateWindow("SDL Test",
                                  SDL_WINDOWPOS_UNDEFINED,
                                  SDL_WINDOWPOS_UNDEFINED,
                                  640,
                                  480,
                                  0);
        if(!window)
        {
            SDL_Log("Failed to create window! SDL_GetError: %s\n", SDL_GetError());
            Success = 0;
        }
        else
        {
            renderer= SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
            if(!renderer)
            {
                SDL_Log("Failed to create renderer!\n");
                Success = 0;
            }
            else
            {
                SDL_SetRenderDrawColor(renderer, 0xff, 0xff, 0xff, 0xff);


            }
        }
    }

    return Success;
}
