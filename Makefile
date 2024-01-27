CC := gcc
CFLAGS := -I/usr/include/SDL2 -D_REENTRANT
LDFLAGS := -lSDL2 -lSDL2_ttf -lSDL2_image

all: main

main: main.c
	$(CC) $(CFLAGS) main.c -o main $(LDFLAGS)

clean:
	rm -f main
