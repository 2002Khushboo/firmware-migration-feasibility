def generate_migration_notes(detected):

    notes = []

    if detected["SPI"]:
        notes.append("SPI detected. Configure equivalent SPI module in TI SysConfig.")

    if detected["UART"]:
        notes.append("UART detected. Map STM UART to TI UART driverlib module.")

    if detected["I2C"]:
        notes.append("I2C detected. Reconfigure I2C in TI environment.")

    if detected["ADC"]:
        notes.append("ADC detected. Verify resolution and sampling differences.")

    if detected["TIMERS"]:
        notes.append("Timers detected: " + ", ".join(detected["TIMERS"]))
        notes.append("Map STM TIM modules to TI Timer/PWM modules.")

    if detected["INTERRUPTS"]:
        notes.append("Interrupts detected. Interrupt vector mapping required.")

    if detected["CLOCK_CONFIG"]:
        notes.append("System clock configuration detected. Redesign clock tree in TI.")

    if detected["DIRECT_REGISTER"]:
        #notes.append("Direct register access found. Manual rewrite required.")
        notes.append("Direct Register Access Analysis:")

        if detected["CLOCK_REGISTER_LINES"]:
            notes.append("- RCC clock configuration registers detected.")
            notes.append("- Appears inside clock calculation logic.")
            #notes.append("- Migration impact: LOW (Clock tree must be redesigned on TI).")

        if detected["APP_REGISTER_LINES"]:
            notes.append("- Application-level peripheral register manipulation detected.")
            notes.append("- Manual rewrite required for TI driver model.")
            #notes.append("- Migration impact: HIGH.")

    return notes