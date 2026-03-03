import re

def detect_features(files_content):
    detected = {
        "GPIO": False,
        "SPI": False,
        "UART": False,
        "I2C": False,
        "ADC": False,
        "DMA": False,
        "TIMERS": [],
        "INTERRUPTS": [],
        "CALLBACKS": [],
        "UART_APIS": [],
        "ADC_APIS": [],
        "CLOCK_CONFIG": False,
        "DIRECT_REGISTER": False,
        "DIRECT_REGISTER_LINES": [],
        "CLOCK_REGISTER_LINES": [],
        "APP_REGISTER_LINES": []
    }

    # Smart direct register pattern
    register_pattern = re.compile(
        r"\b(RCC|GPIO|USART|ADC|TIM|DMA|FDCAN)[0-9]*->"
    )

    for content in files_content:

        if "HAL_GPIO_Init" in content:
            detected["GPIO"] = True

        if "HAL_SPI_Init" in content:
            detected["SPI"] = True

        if "HAL_UART_Init" in content:
            detected["UART"] = True

        if "HAL_I2C_Init" in content:
            detected["I2C"] = True

        if "HAL_ADC_Init" in content:
            detected["ADC"] = True

        if "SystemClock_Config" in content:
            detected["CLOCK_CONFIG"] = True

        #if "RCC->" in content or "GPIOA->" in content:
        #    detected["DIRECT_REGISTER"] = True

        if "HAL_DMA_Init" in content or re.search(r"\bHAL_DMA_\w+\s*\(", content):
            detected["DMA"] = True

        # Detect Timer instances
        timer_matches = re.findall(r"MX_(TIM\d+)_Init", content)
        for match in timer_matches:
            if match not in detected["TIMERS"]:
                detected["TIMERS"].append(match)

        # Detect Interrupt Handlers
        irq_matches = re.findall(r"void\s+(\w+_IRQHandler)", content)
        for irq in irq_matches:
            if irq not in detected["INTERRUPTS"]:
                detected["INTERRUPTS"].append(irq)
        
        callback_matches = re.findall(r"\b(HAL_\w+Callback)\b", content)
        for cb in callback_matches:
            if cb not in detected["CALLBACKS"]:
                detected["CALLBACKS"].append(cb)

        uart_calls = re.findall(r"\b(HAL_UART_\w+)\s*\(", content)
        for call in uart_calls:
            if call not in detected["UART_APIS"]:
                detected["UART_APIS"].append(call)

        adc_calls = re.findall(r"\b(HAL_ADC_\w+)\s*\(", content)
        for call in adc_calls:
            if call not in detected["ADC_APIS"]:
                detected["ADC_APIS"].append(call)
    
        # -------- Direct Register Detection (SMART) --------
        for line in content.splitlines():
            if register_pattern.search(line):

                detected["DIRECT_REGISTER"] = True
                clean_line = line.strip()

                # Limit storage
                if len(detected["DIRECT_REGISTER_LINES"]) < 200:
                    detected["DIRECT_REGISTER_LINES"].append(clean_line)

                # -------- Classification --------

                # Clock-related registers
                if "RCC->" in clean_line:
                    if clean_line not in detected["CLOCK_REGISTER_LINES"]:
                        detected["CLOCK_REGISTER_LINES"].append(clean_line)

                # Application-level peripheral registers
                elif any(x in clean_line for x in ["GPIO", "TIM", "USART", "ADC", "DMA", "FDCAN"]):
                    if clean_line not in detected["APP_REGISTER_LINES"]:
                        detected["APP_REGISTER_LINES"].append(clean_line)

    return detected