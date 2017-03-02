const Lab = {
    THIRD: 'third',
    BASEMENT: 'basement',
};
class LabsResponse {
    constructor(json) {
        this.machines = {};
        this.success = json["meta"]["success"];
        if (!json["meta"]["success"]) {
            return;
        }
        const values = json["values"];
        for (let i = 0; i < values.length; i++) {
            const machine = values[i];
            this.machines[machine.name] = machine;
        }
    }

    getByLab() {
        let byLab = {};
        const keys = Object.keys(this.machines);
        for (let i = 0; i < keys.length; i++) {
            const machine = this.machines[keys[i]];
            if (byLab[machine.lab] !== undefined) {
                byLab[machine.lab].push(machine);
            } else {
                byLab[machine.lab] = [machine];
            }
        }
    }

    getNumMachines(labName) {
        const byLab = this.getByLab();
        return byLab[labName].length;
    }


    getNumOccupied(labName) {
        let total = 0;
        const keys = Object.keys(this.machines);
        for (let i = 0; i < keys.length; i++) {
            const machine = this.machines[keys[i]];
            if (machine.lab === labName && machine.occupied) {
                total += 1;
            }
        }
        return total;
    }

}


class LabsLayoutResponse {

    constructor(json) {
        this.names = [];
        this.labLayout = [];
        this.dimensions = [];
        this.success = json["meta"]["success"];
        if (!json["meta"]["success"]) {
            return;
        }
        const values = json["values"];
        for (let i = 0; i < values.length; i++) {
            let lab = values[i];
            this.names.push(lab["name"]);
            const rawDimensions = lab["dimensions"];
            const dimensions = [Math.round(rawDimensions["width"]), Math.round(rawDimensions["height"])];
            this.dimensions.push(dimensions);
            const machines = lab["layout"];
            const layout = [];
            for (let j = 0; j < machines.length; j++) {
                const entry = machines[j];
                let name = entry["name"];
                let x = entry["x"] / dimensions[0];
                let y = entry["y"] / dimensions[1];
                layout[name] = {name: name, x: x, y: y, isMonitor: name.includes("monitor")};
            }
            this.labLayout.push(layout);
        }

    }

    getAllLayouts() {
        return Object.assign(this.machines[0], this.machines[1])
    }
}

class LabMachine {
    constructor(name, x, y) {
        this.name = name;
        this.x = x;
        this.y = y;
    }
}
