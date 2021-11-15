#!/bin/bash

PLANSZA=("." "." "." "." "." "." "." "." ".")
KONIEC="0"
GRACZ="O"

function wyswietl {
	clear 
	echo "Plansza"
	echo "    0 1 2"
	echo "0   ${PLANSZA[0]} ${PLANSZA[1]} ${PLANSZA[2]}"
	echo "1   ${PLANSZA[3]} ${PLANSZA[4]} ${PLANSZA[5]}"
	echo "2   ${PLANSZA[6]} ${PLANSZA[7]} ${PLANSZA[8]}"
}

function sprawdz_kombinacje {
  if [ ${PLANSZA[$1]} != "." ] && [ ${PLANSZA[$1]} == ${PLANSZA[$2]} ] && [ ${PLANSZA[$2]} == ${PLANSZA[$3]} ]; then
    KONIEC=1
  fi
}

function sprawdz_wygrana {
	sprawdz_kombinacje 0 1 2
	sprawdz_kombinacje 3 4 5
	sprawdz_kombinacje 6 7 8
	sprawdz_kombinacje 0 3 6
	sprawdz_kombinacje 1 4 7
	sprawdz_kombinacje 2 5 8
	sprawdz_kombinacje 0 4 8
	sprawdz_kombinacje 2 4 6
}

function sprawdz_remis {
	if [ ${PLANSZA[0]} != "." ] && [ ${PLANSZA[1]} != "." ] && [ ${PLANSZA[2]} != "." ] && 
	[ ${PLANSZA[3]} != "." ] && [ ${PLANSZA[4]} != "." ] && [ ${PLANSZA[5]} != "." ] && 
	[ ${PLANSZA[6]} != "." ] && [ ${PLANSZA[7]} != "." ] && [ ${PLANSZA[8]} != "." ]; then
		KONIEC=2
	fi
}

function zmiana_gracza {
  	if [ ${GRACZ} = "O" ] && [ $KONIEC -eq 0 ]; then
    	GRACZ="X"
	else
		GRACZ="O"
  	fi
}

function ustaw_pole {
	idx=$(( $1 * 3 + $2 ))
	if [ ${PLANSZA[$idx]} = "." ]; then 
		PLANSZA[$idx]=$GRACZ
		wyswietl
		sprawdz_remis
		sprawdz_wygrana
		if [ $KONIEC -eq 0 ]; then 
			zmiana_gracza
		fi
	else
		wyswietl
		echo "Tu nie wolmo!"
	fi
}

wyswietl
while [ $KONIEC -eq 0 ]
do
	read X Y
	if [ -n $X ] && [ -n $Y ]; then
		ustaw_pole $X $Y
	fi
done

if [ $KONIEC -eq 1 ]; then 
	echo "Wygral Pan $GRACZ GZ!!"
else
	echo "Remisu"
fi