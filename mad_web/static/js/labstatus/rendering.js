function renderTooltips(spaces, spaceTipTemplate, monitorTipTemplate) {

    function renderTooltip(data) {
        const templateData = {data: data};
        _.templateSettings.variable = "data";
        return spaceTipTemplate(templateData)
    }

    function renderMonitorTooltip(data) {
        const templateData = {data: data};
        _.templateSettings.variable = "data";
        return monitorTipTemplate(templateData)

    }

    for (let i = 0; i < spaces.length; i++) {
        const space = spaces[i];
        const classes = space.className;

        let tooltipContent;
        if (classes.includes("monitor")) {
            const data = space.dataset;
            tooltipContent = renderMonitorTooltip(data);
        } else {
            const data = space.dataset;
            tooltipContent = renderTooltip(data);
        }

        $(space).tooltipster({
            content: $(tooltipContent),
            theme: "tooltip",
            speed: 200,
            trigger: "hover",
            // Using the click trigger may be helpful for debugging styles
            //trigger: "click"
        });
    }
}

function renderSpaces(spaces, container, spaceTemplate) {
    function renderSpace(data) {
        const templateData = {data: data};
        _.templateSettings.variable = "data";
        return spaceTemplate(templateData)
    }

    const keys = Object.keys(spaces);
    for (let i = 0; i < keys.length; i++) {
        const space = spaces[keys[i]];
        const machine = {location: space, name: keys[i]};
        container.append(renderSpace(machine));
    }
}

function updateMachineInfo(info, spaces) {
    for (let i = 0; i < spaces.length; i++) {
        const space = $(spaces[i]);
        const name = space.data('name');
        const machineInfo = info[name];
        if (machineInfo) {
            space.attr('data-users', machineInfo.users);
            space.attr('data-load', machineInfo.load);
            space.attr('data-uptime', machineInfo.uptime);
            space.attr('data-occupied', machineInfo.occupied);
            space.attr('data-up', machineInfo.up);
        }
    }
}

function positionSpaces(spaces) {
    for (let i = 0; i < spaces.length; i++) {
        const element = spaces[i];
        const data = element.dataset;
        element.style.left = data.xPercent * 100.0 + "%";
        element.style.top = data.yPercent * 100.0 + "%";

    }
}
