from rich.console import Console

while True:

    console = Console()
    ans = console.input("1)geef hallo , 2) geef wereld , 3) geef doei , 4) geef len , 0) om te stoppen : [bold magenta][1/2/3/4/0][/bold magenta] ")
    
    match ans:
        case "1":
            print("hallo wereld")
        case "2":
            print("wereld is fucked")
        case "3":
            print("doei mensen!")
        case "4":
            print("Len is Emma aan het math.sqrten")
        case "0":
            quit()
            
        

    