#!/bin/bash

PLANSZA=("." "." "." "." "." "." "." "." ".")
KONIEC="0"
GRACZ="O"
RE_NUM='^[0-9]$'
RE_SAVE='^save-.+\.txt$'
SAVE=""

function legenda {
	echo "   Legenda"
	echo "Q - zkoncz gre"
	echo "S - zapisz gre"
	echo
}

function wyswietl {
	clear
	legenda
	echo "Plansza    ruch $GRACZ"
	echo "    0 1 2"
	echo "0   ${PLANSZA[0]} ${PLANSZA[1]} ${PLANSZA[2]}"
	echo "1   ${PLANSZA[3]} ${PLANSZA[4]} ${PLANSZA[5]}"
	echo "2   ${PLANSZA[6]} ${PLANSZA[7]} ${PLANSZA[8]}"
	echo
}

function sprawdz_kombinacje {
  if [ ${PLANSZA[$1]} != "." ] && [ ${PLANSZA[$1]} == ${PLANSZA[$2]} ] && [ ${PLANSZA[$2]} == ${PLANSZA[$3]} ]
  then
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
	[ ${PLANSZA[6]} != "." ] && [ ${PLANSZA[7]} != "." ] && [ ${PLANSZA[8]} != "." ]
	then
		KONIEC=2
	fi
}

function zmiana_gracza {
  	if [ ${GRACZ} = "O" ] && [ $KONIEC -eq 0 ]
	then
    	GRACZ="X"
	else
		GRACZ="O"
  	fi
}

function ustaw_pole {
	idx=$(( $2 * 3 + $1 ))
	if [ ${PLANSZA[$idx]} = "." ]
	then 
		PLANSZA[$idx]=$GRACZ
		sprawdz_remis
		sprawdz_wygrana
		if [ $KONIEC -eq 0 ]
		then 
			zmiana_gracza
		fi
		wyswietl
	else
		wyswietl
		echo "Tu nie wolno!"
	fi
}

function zakoczenie {
	if [ $KONIEC -eq 1 ]
	then 
		echo "Wygral Pan $GRACZ GZ!!"
	elif [ $KONIEC -eq 2 ]
	then
		echo "Remis"
	elif [ $KONIEC -eq 3 ]
	then
		echo "Zapisano grę pod nazwą: $SAVE"
	elif [ $KONIEC -eq 4 ]
	then
		echo "Koniec"
	fi
}

function zapisz {
	SAVE="save-$(date +%Y-%m-%d-%H-%M-%S).txt"
	n=0
	while [ $n -le 8 ]
	do
		echo ${PLANSZA[$n]} >> $SAVE
		n=$(( $n + 1 ))
	done 
	echo $GRACZ >> $SAVE
}

function gra {
	wyswietl
	while [ $KONIEC -eq 0 ]
	do
		echo "Podaj pozycje X Y lub wartosc z legendy:"
		read X Y
		if [[ $X =~ $RE_NUM ]] && [ $X -ge 0 ] && [ $X -le 2 ] && 
		[[ $Y =~ $RE_NUM ]] && [ $Y -ge 0 ] && [ $Y -le 2 ]
		then
			echo $X
			echo $Y
			ustaw_pole $X $Y
		elif [[ $X =~ ^[s]$ ]] || [[ $X =~ ^[S]$ ]]
		then
			KONIEC=3
			zapisz
		elif [[ $X =~ ^[q]$ ]] || [[ $X =~ ^[Q]$ ]]
		then
			KONIEC=4
		else
			wyswietl
			echo "Podano zle wartosci"
		fi
	done
	zakoczenie
}

function wczytaj {
	n=0
	while read line
	do
		if [ $n -le 8 ]
		then
			PLANSZA[$n]=$line
			n=$(( $n + 1 ))
		else
			GRACZ=$line
		fi
	done < $SAVE
}

if [[ $1 =~ $RE_SAVE ]]
then
	SAVE=$1
	wczytaj
fi

wyswietl
gra