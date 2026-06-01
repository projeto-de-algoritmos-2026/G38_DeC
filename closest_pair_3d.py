from dataclasses import dataclass
from math import sqrt
from random import uniform, randint
from typing import Callable

from vpython import button, canvas, color, label, rate, sphere, vector, curve


@dataclass(frozen=True)
class Point3D:
    """Representa um ponto no espaco tridimensional."""

    id: int
    x: float
    y: float
    z: float

    def as_vector(self) -> vector:
        return vector(self.x, self.y, self.z)


@dataclass(frozen=True)
class ClosestPairResult:
    first: Point3D
    second: Point3D
    distance: float
    comparisons: int
    complexity: str


@dataclass(frozen=True)
class PointGraphic:
    point: Point3D
    body: sphere


POINTS: list[Point3D] = []
POINT_GRAPHICS: dict[int, PointGraphic] = {}
ACTIVE_OVERLAYS: list[object] = []
STATUS_LABEL: label | None = None
SCENE: canvas | None = None


def distance_3d(first: Point3D, second: Point3D) -> float:
    """Calcula a distancia euclidiana 3D entre dois pontos."""

    return sqrt(
        (second.x - first.x) ** 2
        + (second.y - first.y) ** 2
        + (second.z - first.z) ** 2
    )


def closest_pair_brute_force(points: list[Point3D]) -> ClosestPairResult:
    """
    Encontra o par de pontos mais proximos por forca bruta.

    Esta funcao fica isolada para que, futuramente, possa ser substituida
    por uma versao mais eficiente usando divisao e conquista.
    """

    if len(points) < 2:
        raise ValueError("Sao necessarios pelo menos dois pontos.")

    closest_first = points[0]
    closest_second = points[1]
    smallest_distance = distance_3d(closest_first, closest_second)
    comparisons = 1

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if i == 0 and j == 1:
                continue

            current_distance = distance_3d(points[i], points[j])
            comparisons += 1

            if current_distance < smallest_distance:
                closest_first = points[i]
                closest_second = points[j]
                smallest_distance = current_distance

    return ClosestPairResult(
        first=closest_first,
        second=closest_second,
        distance=smallest_distance,
        comparisons=comparisons,
        complexity="O(n^2) - forca bruta",
    )


def closest_pair_divide_and_conquer(points: list[Point3D]) -> ClosestPairResult:
    """
    Encontra o par de pontos mais proximos usando divisao e conquista.

    A implementacao divide o conjunto pela coordenada x, resolve cada metade
    recursivamente e depois verifica a faixa central para capturar pares que
    atravessam a divisao.
    """

    if len(points) < 2:
        raise ValueError("Sao necessarios pelo menos dois pontos.")

    points_by_x = sorted(points, key=lambda point: (point.x, point.y, point.z, point.id))
    result = _closest_pair_divide_and_conquer(points_by_x)
    return ClosestPairResult(
        first=result.first,
        second=result.second,
        distance=result.distance,
        comparisons=result.comparisons,
        complexity="O(n log^2 n) - dividir e conquistar",
    )


def _closest_pair_divide_and_conquer(points_by_x: list[Point3D]) -> ClosestPairResult:
    if len(points_by_x) <= 3:
        return closest_pair_brute_force(points_by_x)

    mid_index = len(points_by_x) // 2
    midpoint_x = points_by_x[mid_index].x

    left_result = _closest_pair_divide_and_conquer(points_by_x[:mid_index])
    right_result = _closest_pair_divide_and_conquer(points_by_x[mid_index:])

    best_result = left_result if left_result.distance <= right_result.distance else right_result
    comparisons = left_result.comparisons + right_result.comparisons
    delta = best_result.distance

    strip = [point for point in points_by_x if abs(point.x - midpoint_x) < delta]
    strip.sort(key=lambda point: (point.y, point.z, point.x, point.id))

    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if strip[j].y - strip[i].y >= delta:
                break

            current_distance = distance_3d(strip[i], strip[j])
            comparisons += 1

            if current_distance < delta:
                delta = current_distance
                best_result = ClosestPairResult(
                    first=strip[i],
                    second=strip[j],
                    distance=current_distance,
                    comparisons=comparisons,
                    complexity="O(n log^2 n) - dividir e conquistar",
                )

    return ClosestPairResult(
        first=best_result.first,
        second=best_result.second,
        distance=delta,
        comparisons=comparisons,
        complexity="O(n log^2 n) - dividir e conquistar",
    )


def find_closest_pair(
    points: list[Point3D],
    strategy: Callable[[list[Point3D]], ClosestPairResult] = closest_pair_brute_force,
) -> ClosestPairResult:
    """Ponto unico de entrada para trocar o algoritmo no futuro."""

    return strategy(points)


def generate_random_points(
    amount: int | None = None,
    coordinate_min: float = -10.0,
    coordinate_max: float = 10.0,
) -> list[Point3D]:
    """Gera entre 20 e 50 pontos aleatorios por padrao."""

    total = amount if amount is not None else randint(20, 50)

    return [
        Point3D(
            id=index + 1,
            x=uniform(coordinate_min, coordinate_max),
            y=uniform(coordinate_min, coordinate_max),
            z=uniform(coordinate_min, coordinate_max),
        )
        for index in range(total)
    ]


def format_point(point: Point3D) -> str:
    return f"P{point.id} = ({point.x:.2f}, {point.y:.2f}, {point.z:.2f})"


def print_result(points: list[Point3D], result: ClosestPairResult) -> None:
    """Exibe os dados principais no console."""

    print("\n=== Par de Pontos Mais Proximos em 3D ===")
    print(f"Quantidade de pontos: {len(points)}")
    print(f"Primeiro ponto: {format_point(result.first)}")
    print(f"Segundo ponto: {format_point(result.second)}")
    print(f"Menor distancia encontrada: {result.distance:.4f}")
    print(f"Comparacoes realizadas: {result.comparisons}")
    print(f"Complexidade do algoritmo usado: {result.complexity}")


def create_scene() -> canvas:
    """Cria a janela/cena 3D do VPython."""

    scene = canvas(
        title="Par de Pontos Mais Proximos em 3D",
        width=1000,
        height=650,
        background=color.gray(0.08),
    )
    scene.camera.pos = vector(0, 0, 35)
    scene.camera.axis = vector(0, 0, -35)
    scene.range = 14
    return scene


def register_controls(scene: canvas) -> None:
    """Cria os botões para escolher o algoritmo."""

    scene.append_to_caption("\nEscolha o algoritmo:\n")
    button(text="Forca bruta", bind=on_brute_force_click)
    scene.append_to_caption("  ")
    button(text="Dividir e conquistar", bind=on_divide_and_conquer_click)
    scene.append_to_caption("\n\n")


def create_base_point_graphics(points: list[Point3D]) -> None:
    """Cria as esferas dos pontos uma unica vez."""

    POINT_GRAPHICS.clear()
    for point in points:
        POINT_GRAPHICS[point.id] = PointGraphic(
            point=point,
            body=sphere(
                pos=point.as_vector(),
                radius=0.25,
                color=color.cyan,
                emissive=False,
            ),
        )


def clear_active_overlays() -> None:
    """Remove linhas, labels e destaques anteriores."""

    global STATUS_LABEL

    for overlay in ACTIVE_OVERLAYS:
        if hasattr(overlay, "visible"):
            overlay.visible = False
    ACTIVE_OVERLAYS.clear()

    if STATUS_LABEL is not None and hasattr(STATUS_LABEL, "visible"):
        STATUS_LABEL.visible = False
        STATUS_LABEL = None


def apply_result_visuals(result: ClosestPairResult) -> None:
    """Atualiza as esferas e desenha os elementos do resultado atual."""

    clear_active_overlays()

    for graphic in POINT_GRAPHICS.values():
        graphic.body.radius = 0.25
        graphic.body.color = color.cyan
        graphic.body.emissive = False

    highlighted_ids = {result.first.id, result.second.id}
    for point_id in highlighted_ids:
        graphic = POINT_GRAPHICS[point_id]
        graphic.body.radius = 0.42
        graphic.body.color = color.red
        graphic.body.emissive = True

        point = graphic.point
        point_label = label(
            pos=point.as_vector() + vector(0, 0.75, 0),
            text=f"P{point.id}",
            height=15,
            box=False,
            opacity=0,
            color=color.white,
        )
        ACTIVE_OVERLAYS.append(point_label)

    connection = curve(
        pos=[result.first.as_vector(), result.second.as_vector()],
        color=color.yellow,
        radius=0.045,
    )
    ACTIVE_OVERLAYS.append(connection)

    midpoint = (result.first.as_vector() + result.second.as_vector()) / 2
    global STATUS_LABEL
    STATUS_LABEL = label(
        pos=midpoint + vector(0, 1.0, 0),
        text=f"Menor distancia: {result.distance:.4f}",
        height=16,
        box=True,
        border=8,
        color=color.yellow,
        background=color.black,
    )
    ACTIVE_OVERLAYS.append(STATUS_LABEL)


def execute_strategy(
    strategy_name: str,
    strategy: Callable[[list[Point3D]], ClosestPairResult],
) -> None:
    """Executa um algoritmo e atualiza o console e a visualizacao."""

    result = find_closest_pair(POINTS, strategy)
    apply_result_visuals(result)
    print_result(POINTS, result)
    if SCENE is not None:
        SCENE.title = f"Par de Pontos Mais Proximos em 3D - {strategy_name}"


def on_brute_force_click(_event: object | None = None) -> None:
    execute_strategy("Forca bruta", closest_pair_brute_force)


def on_divide_and_conquer_click(_event: object | None = None) -> None:
    execute_strategy("Dividir e conquistar", closest_pair_divide_and_conquer)


def main() -> None:
    global POINTS, SCENE

    POINTS = generate_random_points()
    SCENE = create_scene()
    register_controls(SCENE)
    create_base_point_graphics(POINTS)
    execute_strategy("Forca bruta", closest_pair_brute_force)

    while True:
        rate(30)


if __name__ == "__main__":
    main()
