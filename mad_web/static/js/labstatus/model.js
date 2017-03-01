const Lab = {
    THIRD: 'third',
    BASEMENT: 'basement',
};
class LabsResponse {
    constructor(json) {
        this.machines = [{}, {}];
        this.success = json["meta"]["success"];
        if (json["meta"]["success"]) {
            const values = json["values"];
            for (let i = 0; i < values.length; i++) {
                const machine = values[i];
                if (machine.lab == "third") {
                    this.machines[0][machine.name] = machine;
                } else {
                    this.machines[1][machine.name] = machine
                }
            }
        }
    }
}


class LabsLayoutResponse {

    constructor(json) {
        this.machines_layout = [{}, {}];
        this.dimensions = [];
        this.success = json["meta"]["success"];
        if (json["meta"]["success"]) {
            let third = json["values"][0];
            let basement = json["values"][1];
            let third_dimensions = third["dimensions"];
            let basement_dimensions = basement["dimensions"];
            this.dimensions.push(
                [Math.round(third_dimensions["width"]), Math.round(third_dimensions["height"])]);
            this.dimensions.push(
                [Math.round(basement_dimensions["width"]), Math.round(basement_dimensions["height"])]);
            const third_machines = third["layout"];
            const basement_machines = basement["layout"];
            for (let i = 0; i < third_machines.length; i++) {
                const entry = third_machines[i];
                let name = entry["name"];
                let x = entry["x"];
                let y = entry["y"];
                this.machines_layout[0][name] = [x / this.dimensions[0][0], y / this.dimensions[0][1]];
                entry.is_monitor = name.includes("monitor");
            }

            for (let i = 0; i < basement_machines.length; i++) {
                const entry = basement_machines[i];
                let name = entry["name"];
                let x = entry["x"];
                let y = entry["y"];
                this.machines_layout[1][name] = [x / this.dimensions[0][0], y / this.dimensions[0][1]];
                entry.is_monitor = name.includes("monitor");
            }
        }
    }
}

class LabMachine {
    constructor(name, x, y) {
        this.name = name;
        this.x = x;
        this.y = y;
    }
}
