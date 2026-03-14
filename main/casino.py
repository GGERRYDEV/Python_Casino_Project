import random
import time
import os



dinero = int(5000)

def apuesta():
    global cantidad
    global dinero
    print(f"You have {dinero}€")
    print("How much do you want to bet?")
    cantidad = input()
    if not cantidad.isdigit():
        print("Invalid quantity.")
        return 0
    
    cantidad = int(cantidad)

    if cantidad > dinero:
        print("You can't bet that amount.")
        return dinero
    else:
        return cantidad

def perder():
    global dinero
    if dinero <= 0:
        print("You've run out of money...")
        exit()
    else:      
        limpiar()
        inicio()

def inicio():
    while True:
        print("Welcome to the python casino!")
        print(f"You have {dinero}€")
        print("We have these games:")
        print("1. Roulette")
        print("2. Slot machine")
        print("3. Blackjack")
        print("4. Dice")
        print("5. Loop")
        print("Choose one with numbers or with the name")

        juego = input()

        if juego == "Roulette" or juego == "1":
            ruleta()
        elif juego == "Slot machine" or juego == "2":
            tragaperras() 
        elif juego == "Blackjack" or juego == "3":
            blackjack()
        elif juego == "Dice" or juego == "4":
            dados()
        elif juego == "Loop" or juego == "5":
            loop()
        else:
            print("Unrecognized option")





def girando():
    for i in range(36):
        limpiar()
        numero, emoji = random.choice(colores_ruleta)
        print("🎰Spinning🎰")
        print(f"🎲 {numero} {emoji} 🎲")
        time.sleep(i * 0.015)

    if numero == 0:
        color = "Green"
    elif emoji == "🟥":
        color = "Red"
    else:
        color = "Black"

    par = numero % 2 == 0
    alto = 19 <= numero <= 36

    limpiar()
    print(f"The number is {numero}{emoji} and is the colour {color}!")
    time.sleep(2)
    return numero, color, par, alto
def ruleta():

    global cantidad
    global dinero
    eleccion_n = 0
    cantidad = apuesta()
    limpiar()
    print(f"You have bet {cantidad}€")
    time.sleep(1)
    print("You can choose between:")
    print("Number (X36)")
    print("Red (X2)")
    print("Black (X2)")
    print("Green (X36)")
    print("Pair (X2)")
    print("Odd (X2)")
    print("High (19-36, X2)")
    print("Low (1-18, X2)")
    eleccion = input()
    if eleccion == "Number":
        print("Choose a number")
        eleccion_n == int(input())
        if eleccion_n > 36:
            print("You can't choose that number")
        else:
            numero, color, par, alto = girando()
            if eleccion == "Red":
                if color == "Red":
                    print(f"You won {cantidad * 2}€")
                    dinero -= cantidad
                    dinero += cantidad * 2
                else:
                    print(f"You have lost {cantidad}€")
                    dinero -= cantidad
            elif eleccion == "Number":
                if eleccion_n == numero:
                    print(f"You won {cantidad * 36}€")
                    dinero -= cantidad
                    dinero += cantidad * 36
                else: 
                    print(f"You have lost {cantidad}€")
                    dinero -= cantidad
            elif eleccion == "Black":
                if color == "Black":
                    print(f"You won {cantidad * 2}€")
                    dinero -= cantidad
                    dinero += cantidad * 2
                else: 
                    print(f"You have lost {cantidad}€")
                    dinero -= cantidad
            elif eleccion == "Green":
                if color == "Green":
                    print(f"You won {cantidad * 36}€")
                    dinero -= cantidad
                    dinero = cantidad * 36
                else: 
                    print(f"You have lost {cantidad}€")
                    dinero -= cantidad
            elif eleccion == "Pair":
                if par == True:
                    print(f"You won {cantidad * 2}€")
                    dinero -= cantidad
                    dinero += cantidad * 2
                else: 
                    print(f"You have lost {cantidad}€")
                    dinero -= cantidad
            elif eleccion == "Odd":
                if par == False:
                    print(f"You won {cantidad * 2}€")
                    dinero -= cantidad
                    dinero += cantidad * 2
                else: 
                    print(f"You have lost {cantidad}€")
                    dinero -= cantidad
            elif eleccion == "High":
                if alto == True:
                    print(f"You won {cantidad * 2}€")
                    dinero -= cantidad
                    dinero += cantidad * 2
                else: 
                    print(f"You have lost {cantidad}€")
                    dinero -= cantidad
            elif eleccion == "Low":
                if alto == False:
                    print(f"You won {cantidad * 2}€")
                    dinero -= cantidad
                    dinero += cantidad * 2
                else: 
                    print(f"You have lost {cantidad}€")
                    dinero -= cantidad
            time.sleep(2)
            limpiar()
            perder()
    elif eleccion not in elecciones:
        print("Unrecognized option")
    else:
        numero, color, par, alto = girando()
        if eleccion == "Red":
            if color == "Red":
                print(f"You won {cantidad * 2}€")
                dinero -= cantidad
                dinero += cantidad * 2
            else:
                print(f"You have lost {cantidad}€")
                dinero -= cantidad
        elif eleccion == "Number":
            if eleccion_n == numero:
                print(f"You won {cantidad * 36}€")
                dinero -= cantidad
                dinero += cantidad * 36
            else: 
                print(f"You have lost {cantidad}€")
                dinero -= cantidad
        elif eleccion == "Black":
            if color == "Black":
                print(f"You won {cantidad * 2}€")
                dinero -= cantidad
                dinero += cantidad * 2
            else: 
                print(f"You have lost {cantidad}€")
                dinero -= cantidad
        elif eleccion == "Green":
            if color == "Green":
                print(f"You won {cantidad * 36}€")
                dinero -= cantidad
                dinero = cantidad * 36
            else: 
                print(f"You have lost {cantidad}€")
                dinero -= cantidad
        elif eleccion == "Pair":
            if par == True:
                print(f"You won {cantidad * 2}€")
                dinero -= cantidad
                dinero += cantidad * 2
            else: 
                print(f"You have lost {cantidad}€")
                dinero -= cantidad
        elif eleccion == "Odd":
            if par == False:
                print(f"You won {cantidad * 2}€")
                dinero -= cantidad
                dinero += cantidad * 2
            else: 
                print(f"You have lost {cantidad}€")
                dinero -= cantidad
        elif eleccion == "High":
            if alto == True:
                print(f"You won {cantidad * 2}€")
                dinero -= cantidad
                dinero += cantidad * 2
            else: 
                print(f"You have lost {cantidad}€")
                dinero -= cantidad
        elif eleccion == "Low":
            if alto == False:
                print(f"You won {cantidad * 2}€")
                dinero -= cantidad
                dinero += cantidad * 2
            else: 
                print(f"You have lost {cantidad}€")
                dinero -= cantidad
        time.sleep(2)
        limpiar()
        perder()

# TRAGAPERRAS


conteo = {}

def girotragaperras():
    for i in range(36):
        limpiar()
        simbolo1 = random.choice(simbolos)
        simbolo2 = random.choice(simbolos)
        simbolo3 = random.choice(simbolos)
        print("🎰Spinning🎰")
        print(f"{simbolo1} {simbolo2} {simbolo3}")
        time.sleep(i * 0.005)

    lista_simbolos = [simbolo1, simbolo2, simbolo3]
    cantidad_calabazas = lista_simbolos.count("🎃")

    if cantidad_calabazas >= 2:
        premio = "prize is nothing"
        resultado = f"{simbolo1} {simbolo2} {simbolo3}"
        multiplicador = 0
        return premio, resultado, multiplicador

    conteo = {}
    for simbolo in lista_simbolos:
        if simbolo != "🎃":
            if simbolo in conteo:
                conteo[simbolo] += 1
            else:
                conteo[simbolo] = 1

    resultado = f"{simbolo1} {simbolo2} {simbolo3}"

    if cantidad_calabazas == 1:
        for simbolo, cantidad in conteo.items():
            if cantidad == 2:
                if simbolo == '🍒':
                    premio = "x10"
                    multiplicador = 10
                    return premio, resultado, multiplicador
                elif simbolo == '🍋':
                    premio = "x8"
                    multiplicador = 8
                    return premio, resultado, multiplicador
                elif simbolo == '🍉':
                    premio = "x6"
                    multiplicador = 6
                    return premio, resultado, multiplicador
                elif simbolo == '⭐':
                    premio = "x4"
                    multiplicador = 4
                    return premio, resultado, multiplicador
                elif simbolo == '🔔':
                    premio = "x3"
                    multiplicador = 3
                    return premio, resultado, multiplicador
        premio = "nothing"
        multiplicador = 0
        return premio, resultado, multiplicador

    for simbolo, cantidad in conteo.items():
        if cantidad == 3:
            if simbolo == '🍒':
                premio = "x10"
                multiplicador = 10
                return premio, resultado, multiplicador
            elif simbolo == '🍋':
                premio = "x8"
                multiplicador = 8
                return premio, resultado, multiplicador
            elif simbolo == '🍉':
                premio = "x6"
                multiplicador = 6
                return premio, resultado, multiplicador
            elif simbolo == '⭐':
                premio = "x4"
                multiplicador = 4
                return premio, resultado, multiplicador
            elif simbolo == '🔔':
                premio = "x3"
                multiplicador = 3
                return premio, resultado, multiplicador
        elif cantidad == 2:
            premio = "x2"
            multiplicador = 2
            return premio, resultado, multiplicador

    premio = "nothing"
    multiplicador = 0
    return premio, resultado, multiplicador

def tragaperras():
    global dinero
    global cantidad
    limpiar()
    print("Prizes:")
    print("🍒🍒🍒 (X10)")
    print("🍋🍋🍋 (X8)")
    print("🍉🍉🍉 (X6)")
    print("⭐⭐⭐ (X4)")
    print("🔔🔔🔔 (X3)")
    print("🍒🍒🍋 (X2)")
    cantidad = apuesta()
    limpiar()
    print(f"You have bet {cantidad}€")
    time.sleep(1)
    resultado, premio, multiplicador = girotragaperras()
    print(f"The result is {premio}")
    if resultado == "nothing":
        print(f"Your prize is {resultado}")
    else:
        print(f"Your prize is {resultado}€")
    print(f"You won {cantidad * multiplicador}€")
    dinero -= cantidad
    dinero += cantidad * multiplicador
    time.sleep(5)
    perder()

# DADOS

caras = [1,2,3,4,5,6]

def dados():
    global cantidad
    global dinero
    cantidad = apuesta()
    limpiar()
    print(f"You have bet {cantidad}")
    print("Choose a number between 1 al 6")
    print("If you win it will multiply by 2")
    elejido = int(input())
    dado = random.choice(caras)
    if dado == elejido:
        print(f"You won!")
        print(f"Your prize is {cantidad * 2}")
        dinero += cantidad
        time.sleep(3)
    else:
        print(f"You lose, the number was {dado} and yours was {elejido}")
        dinero -= cantidad
        time.sleep(3)
    perder()

# BLACKJACK

def blackjack():
    global cantidad
    global dinero

    def calcular_puntaje(man):
        """Calcula el puntaje de la mano."""
        puntaje = sum([card_values[card] for card in man])
        if "A" in man and puntaje > 21:
            puntaje -= 10 
        return puntaje

    def mostrar_mano(jugador, mano):
        """Muestra la mano de cartas de un jugador."""
        print(f"{jugador}'s hand: {', '.join(mano)} | Score: {calcular_puntaje(mano)}")
    
    cantidad = apuesta() 
    if cantidad == 0:
        return
    
    limpiar()
    print(f"You've bet {cantidad}€")
    time.sleep(1)
    
    random.shuffle(deck)
    jugador_mano = [deck.pop(), deck.pop()]
    dealer_mano = [deck.pop(), deck.pop()]
    
    mostrar_mano("Player", jugador_mano)
    print(f"Dealer's hand: {dealer_mano[0]}, ?")
    
    while calcular_puntaje(jugador_mano) < 21:
        action = input("Do you want to [H]it or [S]tand? ").lower()
        if action == 'h':
            jugador_mano.append(deck.pop())
            mostrar_mano("Player", jugador_mano)
        elif action == 's':
            break
        else:
            print("Invalid choice. Please choose 'H' to hit or 'S' to stand.")
    
    player_score = calcular_puntaje(jugador_mano)
    if player_score > 21:
        print("Player busts! You lose.")
        dinero -= cantidad
        time.sleep(2)
        limpiar()
        perder()
        return
    
    mostrar_mano("Dealer", dealer_mano)
    while calcular_puntaje(dealer_mano) < 17:
        print("Dealer hits...")
        dealer_mano.append(deck.pop())
        mostrar_mano("Dealer", dealer_mano)
        time.sleep(1)
    
    dealer_score = calcular_puntaje(dealer_mano)
    
    if dealer_score > 21:
        print("Dealer busts! You win!")
        dinero += cantidad
    elif player_score > dealer_score:
        print(f"You win! Your score: {player_score}, Dealer's score: {dealer_score}")
        dinero += cantidad
    elif player_score < dealer_score:
        print(f"You lose. Your score: {player_score}, Dealer's score: {dealer_score}")
        dinero -= cantidad
    else:
        print(f"It's a tie! Your score: {player_score}, Dealer's score: {dealer_score}")
    
    time.sleep(2)
    limpiar()
    perder()
def loop():
    global cantidad
    global dinero
    print("Wich game you want to loop it?")
    print("1. Roulette")
    print("2. Slot Machine")
    print("3. Dice")
    loop_game = input()
    eleccion_n = 0
    if loop_game == "1":
        print("How much money do you want to bet for every round?")
        cantidad = int(input())
        print("How many rounds you want?")
        rounds = int(input())
        if cantidad * rounds > dinero:
            print("You don't have enough money to play that many rounds.")
            return
        print("You can choose between:")
        print("Number (X36)")
        print("Red (X2)")
        print("Black (X2)")
        print("Green (X36)")
        print("Pair (X2)")
        print("Odd (X2)")
        print("High (19-36, X2)")
        print("Low (1-18, X2)")
        eleccion = input()
        if eleccion == "Number":
            print("Choose a number")
            eleccion_n == int(input())
            if eleccion_n > 36:
                print("You can't choose that number")
        else:
            i = 0
            list = []
            lost = 0
            win = 0
            for i in range(rounds):
                numero, emoji = random.choice(colores_ruleta)
                result = str(numero) + emoji
                list.append(result)
                if numero == 0:
                    color = "Green"
                elif emoji == "🟥":
                    color = "Red"
                else:
                    color = "Black"
                par = numero % 2 == 0
                alto = 19 <= numero <= 36
                if eleccion == "Red":
                    if color == "Red":
                        win = win + 1
                        dinero -= cantidad
                        dinero += cantidad * 2
                    else:
                        lost = lost + 1
                        dinero -= cantidad
                elif eleccion == "Number":
                    if eleccion_n == numero:
                        win = win + 1
                        dinero -= cantidad
                        dinero += cantidad * 36
                    else: 
                        lost = lost + 1
                        dinero -= cantidad
                elif eleccion == "Black":
                    if color == "Black":
                        win = win + 1
                        dinero -= cantidad
                        dinero += cantidad * 2
                    else: 
                        lost = lost + 1
                        dinero -= cantidad
                elif eleccion == "Green":
                    if color == "Green":
                        win = win + 1
                        dinero -= cantidad
                        dinero = cantidad * 36
                    else: 
                        lost = lost + 1
                        dinero -= cantidad
                elif eleccion == "Pair":
                    if par == True:
                        win = win + 1
                        dinero -= cantidad
                        dinero += cantidad * 2
                    else: 
                        lost = lost + 1
                        dinero -= cantidad
                elif eleccion == "Odd":
                    if par == False:
                        win = win + 1
                        dinero -= cantidad
                        dinero += cantidad * 2
                    else: 
                        lost = lost + 1
                        dinero -= cantidad
                elif eleccion == "High":
                    if alto == True:
                        win = win + 1
                        dinero -= cantidad
                        dinero += cantidad * 2
                    else: 
                        lost = lost + 1
                        dinero -= cantidad
                elif eleccion == "Low":
                    if alto == False:
                        win = win + 1
                        dinero -= cantidad
                        dinero += cantidad * 2
                    else: 
                        lost = lost + 1
                        dinero -= cantidad
        resultado = (win * cantidad) - (lost * cantidad)
        if resultado > 0:
            res = "won"
        elif resultado < 0:
            res = "lost"
        else:
            res = "tied"
        print(f"You won {win} times")
        print(f"You lost {lost} times")
        print(f"You {res} {resultado}€")
        print(list)
        time.sleep(10)
        perder()
    # hi
inicio()
