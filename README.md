# Platform Jumper (PyGame)

2D skákačka, kde hráč skáče po plošinách směrem nahoru. Čím výš se dostaneš, tím vyšší je skóre. Ve hře jsou coiny, nepřátelé, výběr skinu a menu s nastavením i pauzou.

## Funkce

- Skok po plošinách směrem nahoru (auto-jump při dopadu).
- Skóre roste podle dosažené výšky.
- Coiny přidávají bonusové body.
- 5 různých typů nepřátel.
- Výběr skinu s náhledem + nákup skinů za coiny.
- Klikatelné hlavní menu (myš).
- Ukládání peněženky coinů a nejvyššího skóre.
- Speciální plošiny:
  - oranžové zmizí po dopadu
  - zelené boost plošiny tě vyhodí výš
- Pauza během hry.
- Uložení aktivního skinu a stavu hard modu mezi spuštěními.
- Krátká ochrana po zásahu nepřítelem (férovější průběh bez instantních dvojitých hitů).

## Použité knihovny

- `pygame`

## Instalace a spuštění

```bash
pip install -r requirements.txt
python main.py
```

## Ovládání

### Menu

- Primárně myší přes tlačítka (Start, Náhled skinu, Koupit/Použít, Hard mode, Konec)
- `ENTER`, `S` (náhled), `B` (koupit/použít), `H`, `ESC` fungují i klávesnicí

### Ve hře

- `A / D` nebo `LEFT / RIGHT` - Pohyb do stran
- `P` - Pauza / pokračování
- `ESC` - Návrat do menu

### Game Over

- `R` - Restart
- `ESC` - Zpět do menu

## Struktura projektu

```text
hra/
├── main.py
├── requirements.txt
├── README.md
└── src/
    ├── config.py
    ├── game.py
    ├── core/
    │   ├── save_manager.py
    │   └── state.py
    ├── entities/
    │   ├── base_entity.py
    │   ├── player.py
    │   ├── platform.py
    │   └── coin.py
    ├── enemies/
    │   ├── base_enemy.py
    │   └── enemy_types.py
    └── ui/
        └── menu.py
```

## OOP návrh (mapa tříd, dědičnost, polymorfismus)

```text
BaseEntity (pygame.sprite.Sprite)
├── Player
├── Platform
├── Coin
└── Enemy
    ├── WalkerEnemy
    ├── JumperEnemy
    ├── ZigZagEnemy
    ├── ChaserEnemy
    └── SpinnerEnemy

Game (orchestrátor hry)
Menu (vykreslení menu/pauzy/game-over)
Settings (konfigurace)
RuntimeState (běhový stav)
```

### K čemu třídy slouží

- `Game` - hlavní smyčka, stavy hry (`menu`, `running`, `paused`, `game_over`), spawn objektů, kolize, skóre.
- `BaseEntity` - společný základ všech objektů na mapě.
- `Player` - pohyb, gravitace, skok, životy.
- `Platform` - statické plošiny.
- `Coin` - sběratelný objekt pro bonusové body.
- `Enemy` + podtřídy - nepřátelé s různým chováním.
- `Menu` - obrazovky menu/pauza/game over.
- `Settings` - herní nastavení (skin, hard mode).
- `RuntimeState` - průběžné hodnoty (score, coins, výška, game over).

### Kde probíhá polymorfismus

- `BaseEntity.update()` je abstraktní kontrakt; každá podtřída implementuje vlastní `update`.
- `Enemy` podtřídy (`WalkerEnemy`, `JumperEnemy`, `ZigZagEnemy`, `ChaserEnemy`, `SpinnerEnemy`) mají stejné rozhraní, ale odlišné chování pohybu.
- `Game` iteruje přes skupinu nepřátel a volá `update(...)` bez potřeby rozlišovat konkrétní typ.

## Přehled typů nepřátel

1. `WalkerEnemy` - horizontální patrola.
2. `JumperEnemy` - vertikální oscilace.
3. `ZigZagEnemy` - diagonální zig-zag pohyb.
4. `ChaserEnemy` - pronásleduje hráče v ose X.
5. `SpinnerEnemy` - kruhový pohyb kolem počáteční pozice.

## Rozšiřitelnost

- Snadné přidání nového nepřítele: vytvoř novou třídu dědící z `Enemy` a přidej ji do `self.enemy_types` v `Game`.
- Snadné přidání skinu: přidej položku do `SKINS` v `src/config.py`.
