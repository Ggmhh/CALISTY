import aiohttp
import asyncio
import random
from termcolor import colored
import os

def clear_and_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored("""
 ██████╗ █████╗ ██╗     ██╗███████╗████████╗██╗   ██╗
██╔════╝██╔══██╗██║     ██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
██║     ███████║██║     ██║███████╗   ██║    ╚████╔╝ 
██║     ██╔══██║██║     ██║╚════██║   ██║     ╚██╔╝  
╚██████╗██║  ██║███████╗██║███████║   ██║      ██║   
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝   ╚═╝      ╚═╝
                РАЗРАБОТЧИК: @KADICK1   
""", 'light_blue'))

def main():
    clear_and_banner()

    text = input("Введите текст жалобы: ")

    while True:
        num_complaints = input("\nВведите количество жалоб для отправки: ")
        if num_complaints.isdigit():
            num_complaints = int(num_complaints)
            break
        else:
            print(colored("Ошибка: Введите целое число.", 'red'))

    print()

    with open('num.txt', 'r') as num_file:
        contacts = num_file.read().splitlines()

    with open('ua.txt', 'r') as ua_file:
        ua_list = ua_file.read().splitlines()

    url = 'https://telegram.org/support'
    yukino = 0
    success_count = 0
    failure_count = 0
    max_retries = 3

    async def send_complaint(session, text, contact, ua_list):
        nonlocal yukino, success_count, failure_count

        headers = {
            'User-Agent': random.choice(ua_list)
        }
        payload = {
            'text': text,
            'contact': contact
        }

        for attempt in range(max_retries):
            try:
                async with session.post(url, data=payload, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        yukino += 1
                        success_count += 1
                        print(colored(f"Жалоба успешно отправлена: {yukino}", 'green'))
                        return
            except aiohttp.ClientError:
                pass
            except asyncio.TimeoutError:
                pass

        failure_count += 1
        print(colored("Не удалось отправить жалобу после нескольких попыток", 'red'))

    async def run_tasks(num_complaints, text):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(num_complaints):
                chosen_contact = random.choice(contacts)
                tasks.append(send_complaint(session, text, chosen_contact, ua_list))
            await asyncio.gather(*tasks)

    asyncio.run(run_tasks(num_complaints, text))
    print()

    print(colored(f"Успешно отправлено жалоб: {success_count}", 'green'))
    print(colored(f"Не удалось отправить жалоб: {failure_count}", 'red'))
    print()

    input("Нажмите Enter для перезапуска...")
    main()

if __name__ == "__main__":
    main()
