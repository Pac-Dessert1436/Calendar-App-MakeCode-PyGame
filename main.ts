/**
 * This is the main file for your project.
 *
 * Create images, tilemaps, animations, and songs using the
 * asset explorer in VS Code. You can reference those assets
 * using the tagged templates on the assets namespace:
 *
 *     assets.image`myImageName`
 *     assets.tilemap`myTilemapName`
 *     assets.tile`myTileName`
 *     assets.animation`myAnimationName`
 *     assets.song`mySongName`
 *
 * New to MakeCode Arcade? Try creating a new project using one
 * of the templates to learn about Sprites, Tilemaps, Animations,
 * and more! Or check out the reference docs here:
 *
 * https://arcade.makecode.com/reference
 */
namespace CalendarApp {
    const months: string[] = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    const weekdays: string[] = ["S", "M", "T", "W", "T", "F", "S"];

    // Helper function to check leap years
    function isLeapYear(year: number): boolean {
        return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
    }

    // Get starting weekday for any month or year
    function getStartingWeekday(year: number, month: number): number {
        const table = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4];
        const y = month < 3 ? year - 1 : year;
        return (y + Math.floor(y / 4) - Math.floor(y / 100) +
            Math.floor(y / 400) + table[month - 1] + 1) % 7;
    }

    // Get days in month for any year
    function getDaysInMonth(year: number, month: number): number {
        switch (true) {
            case month === 2:
                return isLeapYear(year) ? 29 : 28;
            case [4, 6, 9, 11].indexOf(month) !== -1:
                return 30;
            default:
                return 31;
        }
    }

    export function display(year: number, month: number): void {
        const monthName: string = months[month - 1];
        let heading: TextSprite[] = [
            textsprite.create(monthName, 0, 15),
            textsprite.create(year.toString(), 0, 15)
        ];
        heading[0].setPosition(60, 20);
        heading[1].setPosition(110, 20);
        heading.forEach((item) => { item.setKind(SpriteKind.Text); });

        weekdays.forEach((item, idx) => {
            const text = textsprite.create(item, 0, 15);
            text.setPosition(35 + 15 * idx, 35);
            text.setKind(SpriteKind.Text);
        });

        const startWeekday = getStartingWeekday(year, month);
        const maxDays = getDaysInMonth(year, month);

        let line: number = 0;
        let weekDayIndex: number = startWeekday;
        for (let day = 1; day <= maxDays; day++) {
            let dayRepr: string = day < 10 ? " " + day.toString() : day.toString();
            const dayText = textsprite.create(dayRepr, 0, 15);
            dayText.setPosition(35 + 15 * weekDayIndex, 50 + 10 * line);
            dayText.setKind(SpriteKind.Text);

            weekDayIndex++;
            if (weekDayIndex >= 7) {
                weekDayIndex = 0;
                line++;
            }
        }
    }
}

// on start:
let currentYear = 2024;
let currentMonth = 1;
let needsUpdate = true;

scene.setBackgroundColor(1);

game.onUpdate(() => {
    // Year range validation
    if (currentYear < 1970 || currentYear > 9999) {
        game.showLongText(
            "Year must be between 1970-9999.\nResetting calendar.",
            DialogLayout.Bottom
        );
        game.reset();
    }

    if (needsUpdate) {
        sprites.destroyAllSpritesOfKind(SpriteKind.Text);
        CalendarApp.display(currentYear, currentMonth);
        needsUpdate = false;
    }

    // Year input with "A" button
    if (controller.A.isPressed()) {
        const userInput = game.askForNumber("Jump to year (1970-9999):", 4);
        if (userInput >= 1970 && userInput <= 9999) {
            currentYear = userInput;
            needsUpdate = true;
            game.showLongText(`Jumped to ${userInput}`, DialogLayout.Bottom);
        } else {
            game.showLongText("Please enter between 1970-9999", DialogLayout.Bottom);
        }
        controller.A.setPressed(false);
    }
    // Month navigation with left or right buttons
    if (controller.left.isPressed()) {
        currentMonth--;
        if (currentMonth < 1) {
            currentMonth = 12;
            currentYear--;
        }
        needsUpdate = true;
        controller.left.setPressed(false);
    } else if (controller.right.isPressed()) {
        currentMonth++;
        if (currentMonth > 12) {
            currentMonth = 1;
            currentYear++;
        }
        needsUpdate = true;
        controller.right.setPressed(false);
    }
    // Year navigation with up or down buttons
    if (controller.up.isPressed()) {
        currentYear++;
        needsUpdate = true;
        controller.up.setPressed(false);
    } else if (controller.down.isPressed()) {
        currentYear--;
        needsUpdate = true;
        controller.down.setPressed(false);
    }
});