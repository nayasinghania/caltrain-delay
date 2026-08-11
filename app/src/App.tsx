import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState } from "react"

export function App() {
  const [vehicleId, setVehicleId] = useState("")
  const [stationName, setStationName] = useState("")
  const [delay, setDelay] = useState(0)

  function submit() {
    fetch(`${import.meta.env.VITE_SERVER}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ vehicle_id: Number(vehicleId), station_name: stationName }),
    })
      .then((res) => res.json())
      .then((data) => setDelay(data.result));
  }
  return (
    <div className="flex min-h-svh p-6">
      <div className="flex max-w-md min-w-0 flex-col gap-4 text-sm leading-loose">
        <div>
          <h1>Caltrain Delay Predictor</h1>
          <p>
            Predict train delay times within 1.5 minutes of actual arrival time
          </p>
          <Input
            placeholder="Enter train number"
            value={vehicleId}
            onChange={(e) => setVehicleId(e.target.value)}
          />
          <Input
            placeholder="Enter station name"
            value={stationName}
            onChange={(e) => setStationName(e.target.value)}
          />
          <Button className="mt-2" onClick={submit}>Submit</Button>
          <p className="mt-2">{delay != 0 ? delay.toFixed(2) + " minutes delayed" : "Enter the above information to get a prediction"}</p>
          <p className="mt-2">
            <a
              className="text-primary underline underline-offset-4 transition-colors hover:text-primary/80"
              href="https://www.caltrain.com/schedules/pdfs?active_tab=route_explorer_tab"
            >
              View the official Caltrain schedule
            </a>
          </p>
          <div className="font-mono text-xs text-muted-foreground mt-2">
            (Press <kbd>d</kbd> to toggle dark mode)
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
