package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"slices"
	"strings"
	"time"
)

type Character struct {
	Name         string
	Health       int
	Damage       int
	DodgeChance  float64
	CriticChance float64
}

func (c *Character) Attack(target *Character) AttackResult {
	ar := AttackResult{Attacker: c}
	dmg := c.Damage
	if rand.Float64() < c.CriticChance {
		dmg = dmg * 2
		ar.Crit = true
	}
	ar.Damage = dmg
	if rand.Float64() >= target.DodgeChance {
		target.Health = target.Health - dmg
	} else {
		ar.Dodged = true
	}
	return ar
}

type AttackResult struct {
	Attacker *Character
	Damage   int
	Crit     bool
	Dodged   bool
}

func (ar AttackResult) Describe() string {
	if ar.Dodged {
		return fmt.Sprintf("%s missed!", ar.Attacker.Name)
	} else if ar.Crit {
		return fmt.Sprintf("%s dealt %d critical damage!", ar.Attacker.Name, ar.Damage)
	} else {
		return fmt.Sprintf("%s dealt %d damage!", ar.Attacker.Name, ar.Damage)
	}
}

type UserInterface interface {
	ShowMessage(message string)
	GetInput(prompt string) string
}

type Command struct {
	Keybind     string
	Description string
	Callback    func()
}

type Game struct {
	ui       UserInterface
	chars    map[string]Character
	commands map[string]Command
}

func NewGame(ui UserInterface) Game {
	return Game{
		ui:       ui,
		chars:    make(map[string]Character),
		commands: make(map[string]Command),
	}
}

func (g *Game) RegisterCommand(c Command) {
	g.commands[c.Keybind] = c
}

func (g *Game) RegisterCharacter(ch Character) {
	g.chars[ch.Name] = ch
}

func (g *Game) Run() {
	welcomeMessage := `
░█▀▀░█▀█░░░█▀▄░█░█░█▀▀░█░░░█
░█░█░█░█░░░█░█░█░█░█▀▀░█░░░▀
░▀▀▀░▀▀▀░░░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀

Welcome to the Duel GO version!`
	g.ui.ShowMessage(welcomeMessage)
	for {
		g.showMenu()
		userCommand := g.ui.GetInput("Type your command:")
		command, ok := g.commands[userCommand]
		if !ok {
			g.ui.ShowMessage("Unknown command")
			continue
		}
		command.Callback()
	}
}

func (g *Game) play() {
	char1, char2 := g.chooseChars()
	g.ui.ShowMessage(fmt.Sprintf("\n %s vs %s!\n", char1.Name, char2.Name))
	for {
		time.Sleep(1 * time.Second)
		if char1.Health <= 0 && char2.Health <= 0 {
			g.ui.ShowMessage("Tie!")
			break
		} else if char1.Health > 0 && char2.Health <= 0 {
			g.ui.ShowMessage(fmt.Sprintf("%s won!", char1.Name))
			break
		} else if char2.Health > 0 && char1.Health <= 0 {
			g.ui.ShowMessage(fmt.Sprintf("%s won!", char2.Name))
			break
		}
		g.ui.ShowMessage(char1.Attack(&char2).Describe())
		g.ui.ShowMessage(char2.Attack(&char1).Describe())
		g.ui.ShowMessage("")
	}
}

func (g *Game) showCharacterStats() {
	var b strings.Builder
	fmt.Fprintln(&b, "\nName\tHealth\tDamage\tDodge\tCritical strike")
	for _, ch := range g.chars {
		fmt.Fprintf(&b, "%s\t%d\t%d\t%.0f%%\t%.0f%%\n", ch.Name, ch.Health, ch.Damage, 100*ch.DodgeChance, 100*ch.CriticChance)
	}
	g.ui.ShowMessage(strings.TrimSuffix(b.String(), "\n"))

}

func (g *Game) quit() {
	g.ui.ShowMessage("Bye!")
	os.Exit(0)
}

func (g *Game) showMenu() {
	var b strings.Builder
	fmt.Fprint(&b, "\n")
	for k, c := range g.commands {
		fmt.Fprintf(&b, "%s - %s\n", k, c.Description)
	}
	g.ui.ShowMessage(b.String())
}

func (g *Game) chooseChars() (Character, Character) {
	names := make([]string, 0, 2)
	g.ui.ShowMessage("\nAvailable characters:")
	var b strings.Builder
	for name := range g.chars {
		fmt.Fprint(&b, name, " ")
	}
	g.ui.ShowMessage(b.String() + "\n")
	for len(names) < 2 {
		charName := g.ui.GetInput(fmt.Sprintf("Choose character %d:", len(names)+1))
		if slices.Contains(names, charName) {
			g.ui.ShowMessage("Character names must be unique")
			continue
		}
		if _, ok := g.chars[charName]; !ok {
			g.ui.ShowMessage("Invalid character name")
			continue
		}
		names = append(names, charName)
	}
	char1 := g.chars[names[0]]
	char2 := g.chars[names[1]]
	return char1, char2
}

type StdUI struct{}

func (ui StdUI) ShowMessage(message string) {
	fmt.Println(message)
}

func (ui StdUI) GetInput(prompt string) string {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print(prompt, " ")
	ret, _ := reader.ReadString('\n')
	return strings.Trim(ret, "\n")
}

func main() {
	ui := StdUI{}
	game := NewGame(ui)
	game.RegisterCharacter(Character{
		Name:         "Dodger",
		Health:       100,
		Damage:       10,
		DodgeChance:  0.35,
		CriticChance: 0.05,
	})
	game.RegisterCharacter(Character{
		Name:         "Critier",
		Health:       100,
		Damage:       10,
		DodgeChance:  0.05,
		CriticChance: 0.35,
	})
	game.RegisterCharacter(Character{
		Name:         "Tank",
		Health:       160,
		Damage:       10,
		DodgeChance:  0.01,
		CriticChance: 0.01,
	})
	game.RegisterCommand(Command{
		Keybind:     "p",
		Description: "Play",
		Callback:    func() { game.play() },
	})
	game.RegisterCommand(Command{
		Keybind:     "s",
		Description: "Show character stats",
		Callback:    func() { game.showCharacterStats() },
	})
	game.RegisterCommand(Command{
		Keybind:     "q",
		Description: "Quit",
		Callback:    func() { game.quit() },
	})
	game.Run()
}
