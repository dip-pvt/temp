# ~/.config/i3/config

bar {
    # ... other bar settings ...

    colors {
        # Catppuccin-Frappe colors for i3bar
        # Use 'mantle' for the background
        background              #292c3c

        # Use 'text' for the status line text
        status_line             #c6d0f5

        # Use 'surface1' for separators
        separator               #6e738d

        # You'll also want to theme the window titles based on focus state
        # Format:             border    background    text
        client.focused          #89b4fa   #89b4fa      #232634 # 'blue' border/bg, 'crust' text
        client.unfocused        #303446   #303446      #c6d0f5 # 'base' border/bg, 'text' text
        client.focused_inactive #303446   #303446      #c6d0f5 # 'base' border/bg, 'text' text
        client.urgent           #e78284   #e78284      #232634 # 'red' border/bg, 'crust' text (using 'red' from palette)
        client.placeholder      #303446   #303446      #c6d0f5
        client.background       #303446   #303446      #c6d0f5
    }

    # ... other bar settings ...
}
