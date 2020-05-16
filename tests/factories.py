def workplane_definition_factory():
    return [
        {  # workplane
            "h": {"v": "99999990"},
            "type": "10000",
            "point[0]": {"v": "99999991"},
            "normal": {"v": "99999992"},
        },
        {"h": {"v": "99999991"}, "type": "2000"},  # origin
        {  # normal
            "h": {"v": "99999992"},
            "type": "3000",
            "point[0]": {"v": "99999991"},
            "actNormal": {"w": "1.0"},
        },
    ]


def point_in_3d_definition_factory(hv="99999990", x="0.0", y="0.0", z="0.0"):
    return [{"h": {"v": hv}, "type": "2000", "actPoint": {"x": x, "y": y, "z": z}}]


def point_in_2d_definition_factory(
    hv="99999990", x="0.0", y="0.0", workplane="99999990"
):
    return [
        {
            "h": {"v": hv},
            "type": "2001",
            "actPoint": {"x": x, "y": y},
            "workplane": {"v": workplane},
        }
    ]
