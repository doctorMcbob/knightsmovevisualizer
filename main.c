#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <stdio.h>
#define W 151
#define H 151
#define PW 8

int CELLS[W * H];

int d1 = 0;
int d2 = 0;

int colAlt = 0;

SDL_Color number_to_rgb(int number) {
    // Use prime numbers to generate a pseudo-random sequence
    const int prime1 = 37;
    const int prime2 = 71;
    const int prime3 = 29;

    number -= 1;  // Adjust to 0-indexed
    Uint8 red = (colAlt + number * prime1) % 256;
    Uint8 green = (colAlt + number * prime2) % 256;
    Uint8 blue = (colAlt + number * prime3) % 256;

    SDL_Color color = {red, green, blue, 255};  // 255 for full alpha
    return color;
}

void reset_cells() {
  for (int i = 0; i < W * H; i++) {
    CELLS[i] = 0;
    if (i == W * H / 2) {
      CELLS[i] = 1;
    }
  }
}

int indexAt(int x, int y) {
  if (y * H + x >= W * H) {
    return -1;
  }
  return CELLS[y*H + x];
}

void setAt(int x, int y, int v) {
  if (y * H + x >= W * H) {
    return;
  }
  CELLS[y*H + x] = v;
}

void knight_moves(int x, int y, int arr[]) {
  arr[0] = x + d2; arr[1] = y + d1;
  arr[2] = x + d1; arr[3] = y + d2;
  arr[4] = x - d2; arr[5] = y + d1;
  arr[6] = x - d1; arr[7] = y + d2;
  arr[8] = x + d2; arr[9] = y - d1;
  arr[10] = x + d1; arr[11] = y - d2;
  arr[12] = x - d2; arr[13] = y - d1;
  arr[14] = x - d1; arr[15] = y - d2;
}

void update_grid(int n) {
  int knightMoves[16]; // [x, y, x, y, x, y, ...]
  for (int x = 0; x < W; x++) {
    for (int y = 0; y < H; y++) {
      int c = indexAt(x, y);
      if (c != n) {
	continue;
      }

      knight_moves(x, y, knightMoves);
      for (int i = 0; i < 8; i++) {
	int v = indexAt(i, i+1);
	if (v != 0) {
	  continue;
	}

	setAt(x, y, n + 1);
      }
    }
  }
}

void draw_grid(SDL_Renderer *renderer, TTF_Font *font) {
  SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
  SDL_RenderClear(renderer);

  for (int x = 0; x < W; x++) {
    for (int y = 0; y < H; y++) {
      int c = indexAt(x, y);
      SDL_Color color = number_to_rgb(c);
      if (c == 0) {
	color.r = 255;
	color.g = 255;
	color.b = 255;
      }

      SDL_Rect rect = {x * PW, y * PW, PW, PW};
      SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, 255);
      SDL_RenderFillRect(renderer, &rect);
    }
  }

  char info[100];
  SDL_Surface* surface = TTF_RenderText_Solid(font, info, (SDL_Color){0, 0, 0, 255});
  SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
  SDL_Rect textRect = {0, H * PW, surface->w, surface->h};
  SDL_RenderCopy(renderer, texture, NULL, &textRect);
  
  // Clean up
  SDL_FreeSurface(surface);
  SDL_DestroyTexture(texture);
}

int main(int argc, char* argv[]) {
    SDL_Window* window = NULL;
    SDL_Renderer* renderer = NULL;
    TTF_Font* font = NULL;

    reset_cells();

    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    if (TTF_Init() == -1) {
        printf("SDL_ttf could not initialize! SDL_ttf Error: %s\n", TTF_GetError());
        return 1;
    }

    window = SDL_CreateWindow("SDL Window", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, PW * W, PW * H + 16, SDL_WINDOW_SHOWN);
    if (window == NULL) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    font = TTF_OpenFont("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16); // Ensure the Helvetica font file is available
    if (font == NULL) {
        printf("Failed to load font! SDL_ttf Error: %s\n", TTF_GetError());
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    SDL_Event event;
    int SHOULD_RUN = 1;
    while (SHOULD_RUN) {
      draw_grid(renderer, font);
      
      SDL_RenderPresent(renderer);
      while (SDL_PollEvent(&event)) {
	if (event.type == SDL_QUIT) {
	  SHOULD_RUN = 0;
	} else if (event.type == SDL_KEYDOWN) {
	  switch (event.key.keysym.sym) {
	  case SDLK_q:
	    SHOULD_RUN = 0;
	    break;
	  case SDLK_LEFT:
	    d1 -= 1;
	    break;
	  case SDLK_RIGHT:
	    d1 += 1;
	    break;
	  case SDLK_UP:
	    d2 += 1;
	    break;
	  case SDLK_DOWN:
	    d2 -= 1;
	    break;
	  case SDLK_SPACE: {
	    int n = 1;
	    while (n < 100) {
	      printf("%i\n", n);
	      update_grid(n);
	      n++;
	    }
	    break;
	  }
	  }
	}
      }
    }
        
    // Cleanup
    TTF_CloseFont(font);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    TTF_Quit();
    SDL_Quit();
    
    return 0;
}
