const fs = require('fs');
const BlueLinky = require("bluelinky");


try {
  const bluelinkClient = new BlueLinky({
    username: process.argv[2],
    password: process.argv[3],
    region: "EU",
    pin: process.argv[4]
  })

  bluelinkClient.on("ready", async (theVs) => {
    console.log("BL connected")
    //console.log(theVs)
    
    console.log("1")
    // Get status information for a specific vehicle
    const vehicle = await bluelinkClient.getVehicle(process.argv[5]);
    console.log("2")
    const status = await vehicle.status({ parsed: false, refresh: true });
    
    console.log(status)

  });
   
  console.log("Done")
 
} catch (e) {
  console.log(e.stack)
}


