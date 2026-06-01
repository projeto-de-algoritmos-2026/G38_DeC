from dataclasses import dataclass
from math import sqrt
from random import uniform, randint
from typing import Callable, Iterable

from vpython import canvas, color, label, rate, sphere, vector, curve


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


def print_result(points: Iterable[Point3D], result: ClosestPairResult) -> None:
    """Exibe os dados principais no console."""

    print("\n=== Par de Pontos Mais Proximos em 3D ===")
    print(f"Quantidade de pontos: {len(list(points))}")
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


def render_points(points: list[Point3D], result: ClosestPairResult) -> None:
    """Renderiza as esferas, destaca o par mais proximo e desenha a linha."""

    highlighted_ids = {result.first.id, result.second.id}

    for point in points:
        is_highlighted = point.id in highlighted_ids
        sphere(
            pos=point.as_vector(),
            radius=0.42 if is_highlighted else 0.25,
            color=color.red if is_highlighted else color.cyan,
            emissive=is_highlighted,
        )

        if is_highlighted:
            label(
                pos=point.as_vector() + vector(0, 0.75, 0),
                text=f"P{point.id}",
                height=15,
                box=False,
                opacity=0,
                color=color.white,
            )

    curve(
        pos=[result.first.as_vector(), result.second.as_vector()],
        color=color.yellow,
        radius=0.045,
    )

    midpoint = (result.first.as_vector() + result.second.as_vector()) / 2
    label(
        pos=midpoint + vector(0, 1.0, 0),
        text=f"Menor distancia: {result.distance:.4f}",
        height=16,
        box=True,
        border=8,
        color=color.yellow,
        background=color.black,
    )


def update_closest_pair_highlight(points: list[Point3D]) -> ClosestPairResult:
    """
    Calcula e atualiza o destaque visual.

    Na versao estatica esta funcao roda uma vez. Em uma versao animada, ela
    poderia ser chamada repetidamente apos atualizar as posicoes dos pontos.
    """

    result = find_closest_pair(points)
    render_points(points, result)
    return result


def main() -> None:
    points = generate_random_points()
    create_scene()
    result = update_closest_pair_highlight(points)
    print_result(points, result)

    while True:
        rate(30)


if __name__ == "__main__":
    main()
