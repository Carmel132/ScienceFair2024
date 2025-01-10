#include "game.h"

void Game::run() {

    if(!InitSDL())
    {
        SDL_Log("Failed to initalize!\n");
        return;
    }

    bool quit = false;
    SDL_Event e;
    Renderable* obj = new OutlineColoredRect(50,50, 50,50, Color{0xFF,0,0});
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

        // Render
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0xff);
        SDL_RenderClear(renderer);

                SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xff);

        obj->render(renderer);

        SDL_RenderPresent(renderer);
    }


    // Shutdown
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
	renderer = NULL;
    window =  NULL;

    delete obj;

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
