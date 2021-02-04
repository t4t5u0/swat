package main

import (
	"github.com/gdamore/tcell/v2"
	"github.com/mattn/go-runewidth"
	"github.com/rivo/tview"
)

func main() {
	runewidth.DefaultCondition = &runewidth.Condition{EastAsianWidth: false}
	app := tview.NewApplication()

	// inputField := tview.NewInputField().
	// 	SetLabel("New Character Name:").
	// 	SetFieldWidth(10).SetDoneFunc(func(key tcell.Key) {
	// 	app.Stop()
	// })

	CharacterList := tview.NewList().ShowSecondaryText(false)
	CharacterList.AddItem("ギルバート", "", 0, nil)
	// nil->別ウィンドウを開く関数を置きたい。
	//使い回しになるだろうから、ウィンドウを受け取って、
	CharacterList.AddItem("ルッキオラ", "", 0, nil)
	CharacterList.AddItem("モーラ", "", 0, nil)
	CharacterList.AddItem("New", "", 0, func() {
	})

	CharacterList.SetBorder(true).SetTitle("Character List")
	Status := tview.NewList().ShowSecondaryText(false)
	Status.SetBorder(true).SetTitle("Status")
	MainMenu := tview.NewList().ShowSecondaryText(false)
	MainMenu.SetBorder(true).SetTitle("Menu")
	InputOutput := tview.NewList()
	InputOutput.SetBorder(true).SetTitle("I/O")
	OneLine := tview.NewTextView().SetText("F1 Charater List  F2 Status  F3 Menu  F4 I/O  F5 Setting")
	OneLine.SetBorder(true)

	flex := tview.NewFlex().
		AddItem(tview.NewFlex().SetDirection(tview.FlexRow).
			AddItem(tview.NewFlex().SetDirection(tview.FlexColumn).
				AddItem(tview.NewFlex().SetDirection(tview.FlexRow).
					AddItem(CharacterList, 0, 1, false).
					AddItem(Status, 0, 1, false), 0, 1, false).
				AddItem(tview.NewFlex().SetDirection(tview.FlexRow).
					AddItem(MainMenu, 0, 1, false).
					AddItem(InputOutput, 5, 1, false), 0, 2, false), 0, 1, false).
			AddItem(OneLine, 3, 1, false), 0, 1, false)

	app.SetInputCapture(
		func(event *tcell.EventKey) *tcell.EventKey {
			switch {
			case event.Key() == tcell.KeyF1:
				app.SetFocus(CharacterList)
			case event.Key() == tcell.KeyF2:
				app.SetFocus(Status)
			case event.Key() == tcell.KeyF3:
				app.SetFocus(MainMenu)
			case event.Key() == tcell.KeyF4:
				app.SetFocus(InputOutput)
			}
			return event
		},
	)

	if err := app.SetRoot(flex, true).SetFocus(CharacterList).Run(); err != nil {
		panic(err)
	}
}
