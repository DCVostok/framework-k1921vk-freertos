#include "FreeRTOS.h"
#include "K1921VK01T.h"
#include "niietcm4.h"
#include "retarget_conf.h"
#include "system_K1921VK01T.h"
#include "task.h"

#define UNUSED(x) (void)(x)

#define LED_PIN (GPIO_Pin_8)
#define LED_PORT (NT_GPIOF)

volatile int a = 0;

void LedBlink_task(void *pvParameters) {
  UNUSED(pvParameters);
  while (1) {
    GPIO_ToggleBits(LED_PORT, LED_PIN);
    printf("led state %d\n", (int)GPIO_ReadBit(LED_PORT, LED_PIN));
    a++; // You can use debug breakpoint there to see value of variable
    vTaskDelay(500 / portTICK_PERIOD_MS);
  }
}

void periph_init() {
  SystemCoreClockUpdate();
  retarget_init(); // UART0 used for printf

  GPIO_Init_TypeDef gpio_init_struct;
  GPIO_StructInit(&gpio_init_struct);
  gpio_init_struct.GPIO_AltFunc = GPIO_AltFunc_1;
  gpio_init_struct.GPIO_Dir = GPIO_Dir_Out;
  gpio_init_struct.GPIO_Mode = GPIO_Mode_IO;
  gpio_init_struct.GPIO_Out = GPIO_Out_En;
  gpio_init_struct.GPIO_OutMode = GPIO_OutMode_PP;
  gpio_init_struct.GPIO_Pin = LED_PIN;
  GPIO_Init(LED_PORT, &gpio_init_struct);
}

void freertos_init_objects() {
  xTaskCreate(LedBlink_task, "LedBlink_task", configMINIMAL_STACK_SIZE, NULL,
              configLIBRARY_LOWEST_INTERRUPT_PRIORITY, NULL);
}

//-- Main ----------------------------------------------------------------------
int main() {
  periph_init();
  freertos_init_objects();
  printf("K1921VK01T> All periph inited\n");
  printf("K1921VK01T> CPU frequency is %lu MHz\n", SystemCoreClock / (int)1E6);

  vTaskStartScheduler();
  return 0;
}
