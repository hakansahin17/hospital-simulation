import asyncio
import json
import time
import ssl
import aiohttp
import numpy as np
from datetime import datetime, timedelta

SIMULATION_HOURS = 365 * 24
REAL_TIME_SECONDS = 2 * 3600
SCALE_FACTOR = SIMULATION_HOURS / REAL_TIME_SECONDS

START_DATE = datetime(2024, 1, 1, 9, 0)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def simulate_event(sim_hours, patient_type):
    real_time_delay = sim_hours / SCALE_FACTOR
    await asyncio.sleep(real_time_delay)
    simulated_time = START_DATE + timedelta(hours=sim_hours)

    # Constructing the init parameter as a JSON string
    init_params = json.dumps({
        "patient_type": patient_type,
        "admission_date": int(simulated_time.timestamp())
    })

    # Setting up the payload for the POST request
    payload = {
        "behavior": "fork_running",
        "url": "https://cpee.org/hub/server/Teaching.dir/Prak.dir/Challengers.dir/Hakan_Sahin.dir/Main.xml",
        "init": init_params
    }

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.post("https://cpee.org/flow/start/url/", data=payload) as response:
            response_text = await response.text()
            print(f"API call for {patient_type} patient at simulated time {simulated_time}, response: {response_text}")


def generate_patient_arrivals(distribution, rate, duration, patient_type):
    times = []
    current_time = 0
    while current_time < duration:
        if distribution == "uniform":
            current_time += np.random.uniform(0, rate)
        elif distribution == "exponential":
            current_time += np.random.exponential(scale=rate)
        if current_time < duration:
            times.append(current_time)
    return [(time, patient_type) for time in times]


async def main():
    patient_a = generate_patient_arrivals("uniform", 1, SIMULATION_HOURS, "A")
    patient_b = generate_patient_arrivals("uniform", 1, SIMULATION_HOURS, "B")
    emergency_patients = generate_patient_arrivals("exponential", 1, SIMULATION_HOURS, "EM")

    events = [simulate_event(sim_hour, patient_type) for sim_hour, patient_type in patient_a + patient_b + emergency_patients]
    await asyncio.gather(*events)

if __name__ == "__main__":
    # asyncio.run(simulate_event(0, "A"))
    loop = asyncio.get_event_loop()
    start_time = time.time()
    loop.run_until_complete(main())
    print(f"Simulation completed in {time.time() - start_time} real seconds.")
