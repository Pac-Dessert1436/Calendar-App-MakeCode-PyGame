import pygame
from datetime import datetime, timedelta
import calendar

# Initialize pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame Calendar App")

# Colors
BACKGROUND = (20, 20, 30)
CALENDAR_BG = (40, 40, 60)
HEADER_BG = (30, 30, 50)
TEXT_COLOR = (220, 220, 240)
WEEKEND_COLOR = (255, 100, 100)
WEEKEND_SHADOW = (180, 70, 70)
NORMAL_SHADOW = (60, 60, 90)
NORMAL_DAY = (180, 200, 220)
INACTIVE_DAY = (100, 100, 140)
HEADER_SHADOW = (20, 20, 40)
BUTTON_COLOR = (70, 70, 100)
BUTTON_HOVER = (90, 90, 130)
BUTTON_TEXT = (200, 220, 255)

# Fonts
header_font = pygame.font.SysFont(None, 48)
day_font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 28)

# Month names
month_names = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

# Day names
day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False

    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, HEADER_SHADOW, self.rect, 2, border_radius=8)

        text_surf = small_font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


class CalendarApp:
    def __init__(self):
        self.current_date = datetime.now()
        self.prev_button = Button(150, 80, 120, 40, "Previous")
        self.next_button = Button(530, 80, 120, 40, "Next")
        self.today_button = Button(340, 80, 120, 40, "Today")
    
    def clamp_year_num(self):
        if self.current_date.year < 1970:
            self.current_date = datetime(1970, 1, 1)
        elif self.current_date.year > 9999:
            self.current_date = datetime(9999, 12, 1)

    def prev_month(self):
        # Go to previous month
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(
                year=self.current_date.year-1, month=12)
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month-1)
        self.clamp_year_num()

    def next_month(self):
        # Go to next month
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(
                year=self.current_date.year+1, month=1)
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month+1)
        self.clamp_year_num()

    def go_today(self):
        # Return to current month
        self.current_date = datetime.now()

    def draw(self, surface):
        # Draw background
        surface.fill(BACKGROUND)

        # Draw month/year header
        month_year = f"{month_names[self.current_date.month-1]} {self.current_date.year}"
        month_surf = header_font.render(month_year, True, TEXT_COLOR)
        surface.blit(month_surf, (screen_width//2 -
                     month_surf.get_width()//2, 20))
        
        hint_text = "Navigate by clicking buttons, or with arrow keys or SPACE"
        hint_surf = small_font.render(hint_text, True, (150, 150, 180))
        surface.blit(hint_surf, (screen_width//2 -
                     hint_surf.get_width()//2, 140))

        # Draw buttons
        self.prev_button.draw(surface)
        self.next_button.draw(surface)
        self.today_button.draw(surface)

        # Draw calendar container
        calendar_rect = pygame.Rect(
            50, 180, screen_width-100, screen_height-220)
        pygame.draw.rect(surface, CALENDAR_BG, calendar_rect, border_radius=12)
        pygame.draw.rect(surface, HEADER_SHADOW,
                         calendar_rect, 2, border_radius=12)

        # Draw day headers
        cell_width = (screen_width - 100) // 7
        cell_height = 60
        for i, day in enumerate(day_names):
            x = 50 + i * cell_width
            y = 180

            # Draw day header background
            header_rect = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(surface, HEADER_BG, header_rect)
            pygame.draw.rect(surface, HEADER_SHADOW, header_rect, 1)

            # Draw day name
            color = WEEKEND_COLOR if i == 0 or i == 6 else TEXT_COLOR
            day_surf = small_font.render(day, True, color)
            surface.blit(day_surf, (x + cell_width//2 - day_surf.get_width()//2,
                                    y + cell_height//2 - day_surf.get_height()//2))

        # Calculate calendar days
        first_day = self.current_date.replace(day=1)
        weekday = first_day.weekday()

        # In Python, Monday is 0 and Sunday is 6, but we want Sunday as first day
        # So we adjust: if weekday is 6 (Sunday), set to 0, else add 1
        weekday = (weekday + 1) % 7

        # Get number of days in month
        _, num_days = calendar.monthrange(
            self.current_date.year, self.current_date.month)

        # Get days from previous month
        prev_month = self.current_date - timedelta(days=self.current_date.day)
        _, prev_num_days = calendar.monthrange(
            prev_month.year, prev_month.month)

        # Draw calendar days
        today = datetime.now()
        day_counter = 0

        for row in range(6):
            for col in range(7):
                # Skip days before the first day of the month
                if row == 0 and col < weekday:
                    day_num = prev_num_days - (weekday - col - 1)
                    is_current_month = False
                # Skip days after the last day of the month
                elif day_counter >= num_days:
                    day_num = (day_counter - num_days) + 1
                    is_current_month = False
                    day_counter += 1
                else:
                    day_num = day_counter + 1
                    is_current_month = True
                    day_counter += 1

                x = 50 + col * cell_width
                y = 180 + cell_height + row * cell_height

                # Draw day cell
                cell_rect = pygame.Rect(x, y, cell_width, cell_height)
                pygame.draw.rect(surface, CALENDAR_BG, cell_rect)
                pygame.draw.rect(surface, HEADER_SHADOW, cell_rect, 1)

                # Highlight today
                if (is_current_month and
                    day_num == today.day and
                    self.current_date.month == today.month and
                        self.current_date.year == today.year):

                    highlight_rect = pygame.Rect(
                        x+5, y+5, cell_width-10, cell_height-10)
                    pygame.draw.rect(surface, (80, 100, 150),
                                     highlight_rect, border_radius=8)

                # Determine text color
                if col == 0 or col == 6:  # Weekend
                    shadow_color = WEEKEND_SHADOW if is_current_month else NORMAL_SHADOW
                    text_color = WEEKEND_COLOR if is_current_month else INACTIVE_DAY
                else:
                    shadow_color = NORMAL_SHADOW
                    text_color = NORMAL_DAY if is_current_month else INACTIVE_DAY

                # Draw day number with shadow effect
                day_str = str(day_num)
                shadow_surf = day_font.render(day_str, True, shadow_color)
                text_surf = day_font.render(day_str, True, text_color)

                # Center text in cell
                shadow_pos = (x + cell_width//2 - shadow_surf.get_width()//2 + 1,
                              y + cell_height//2 - shadow_surf.get_height()//2 + 1)
                text_pos = (x + cell_width//2 - text_surf.get_width()//2,
                            y + cell_height//2 - text_surf.get_height()//2)

                surface.blit(shadow_surf, shadow_pos)
                surface.blit(text_surf, text_pos)

    def check_keydown(self, event):
        match event.key:
            case pygame.K_UP:
                self.current_date = self.current_date.replace(
                    year=self.current_date.year+1)
                self.clamp_year_num()
            case pygame.K_DOWN:
                self.current_date = self.current_date.replace(
                    year=self.current_date.year-1)
                self.clamp_year_num()
            case pygame.K_LEFT:
                self.prev_month()
            case pygame.K_RIGHT:
                self.next_month()
            case pygame.K_SPACE:
                self.go_today()
            

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.prev_button.check_hover(mouse_pos)
        self.next_button.check_hover(mouse_pos)
        self.today_button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif self.prev_button.check_click(mouse_pos, event):
                self.prev_month()
            elif self.next_button.check_click(mouse_pos, event):
                self.next_month()
            elif self.today_button.check_click(mouse_pos, event):
                self.go_today()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown(event)

        return True


def main():
    app = CalendarApp()
    clock = pygame.time.Clock()

    running = True
    while running:
        running = app.handle_events()

        app.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
