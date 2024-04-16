CC = cc
CFLAGS = -std=c99 -pedantic -Wall
#OBJECTS = robofocus.o
FFLAGS = 
MANAGER?=homebrew
ifeq ($(MANAGER),homebrew)
        LFLAGS = -L /usr/local/lib -l cfitsio
		#LFLAGS = -L /⁨Users/⁨observer⁩/Desktop/DragonFlyStuff⁩/Software/cfitsio-3.47 -l cfitsio
        INCDIR = /usr/local/include
else
        LFLAGS = -L /opt/local/lib -l cfitsio
        INCDIR = /opt/local/include
endif

#DEPS = 
OBJ = robofocus.o
PROGRAMS = robofocus birger_exec

all: robofocus birger_exec

robofocus.o: birger_main.c $(DEPS)
	$(CC) -c $(CFLAGS) -I${INCDIR} -o $@ $< 

birger_obj.o: birger_main.c $(DEPS)
	$(CC) -c $(CFLAGS) -I${INCDIR} -o $@ $< 

robofocus: robofocus.o 
	$(CC) -o $@ $^ $(FFLAGS) ${LFLAGS}

birger_exec: birger_obj.o 
	$(CC) -o $@ $^ $(FFLAGS) ${LFLAGS}

clean:
	rm -f *.o

install: $(PROGRAMS)
	mv $(PROGRAMS) /usr/local/bin
