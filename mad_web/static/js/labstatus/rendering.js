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
        const data = space.dataset;
        if (classes.includes("monitor")) {
            tooltipContent = renderMonitorTooltip(data);
        } else {
            tooltipContent = renderTooltip(data);
        }
        if (classes.includes("tooltipstered")) {
            $(space).tooltipster('content', $(tooltipContent));
        } else {
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
}

function renderLabs(layoutResponse, container, labTemplate, spaceTemplate) {
    function renderLab(data) {
        const templateData = {data: data};
        _.templateSettings.variable = "data";
        return labTemplate(templateData)
    }

    for (let i = 0; i < layoutResponse.labLayout.length; i++) {
        const layout = layoutResponse.labLayout[i];
        const data = {name: layoutResponse.names[i]};
        container.append(renderLab(data));
        const id = layoutResponse.names[i] + "-lab";
        renderSpaces(layout, $("#" + id + " .machines"), spaceTemplate);
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
        container.append(renderSpace(space));
    }
}

function renderGraphs(stats, containers) {
    const options = {
        backgroundColor: "transparent",
        colors: ['red'],
        legend: {position: 'none'},
        vAxis: {
            textPosition: 'none',
            gridlines: {
                color: 'transparent'
            },
        },
        hAxis: {
            textPosition: 'none',
            gridlines: {
                color: 'transparent'
            }
        },
        axisFontSize: 0
    };
    for (let i = 0; i < stats.length; i++) {
        const data = new google.visualization.DataTable();
        data.addColumn('number', 'X');
        data.addColumn('number', 'Occupied');

        let preparedStats = [];
        for (let j = 0; j < stats[i].length; j++) {
            preparedStats.push([j, stats[i][j]]);
        }
        data.addRows(preparedStats);
        const chart = new google.visualization.LineChart(containers[i]);
        chart.draw(data, options);
    }
}


function updateInfo(labsResponse, spaceTipTemplate, monitorTipTemplate) {
    const spaces = $(".space");
    updateMachineInfo(labsResponse.machines, spaces);
    renderTooltips(spaces, spaceTipTemplate, monitorTipTemplate);
    const labs = $(".lab");
    for (let i = 0; i < labs.length; i++) {
        const lab = labs[i];
        const statsPane = $(lab).find(".stats")[0];
        const name = $(lab).attr("data-name");
        const numOccupied = labsResponse.getNumOccupied(name);
        statsPane.innerHTML = numOccupied + " machines occupied";
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
