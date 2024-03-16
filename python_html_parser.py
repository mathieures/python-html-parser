from html.parser import HTMLParser
from typing import Self


class Element:
    """Classe abstraite représentant un élément HTML."""


class ContentElement(Element):
    """Un Element possédant du contenu, c’est-à-dire une chaîne de caractères."""

    content: str

    def __init__(self, content: str) -> None:
        self.content = content

    def __repr__(self) -> str:
        return "".join((
            "Content<",
            f", content={self.content}" if self.content else "",
            ">"
        ))


class TagElement(Element):
    """Un Element représentant une balise HTML avec des enfants."""

    tag: str
    children: list[Self | ContentElement]

    def __init__(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.attrs = attrs
        self.tag = tag
        self.children = []


    def __repr__(self) -> str:
        children_repr = f"{[repr(child) for child in self.children]}" if self.children else None
        return "".join((
            "Tag<",
            f"tag={self.tag}",
            # f", attrs={self.attrs}" if self.attrs else "",
            # f", children={len(self.children)}" if children_repr else "",
            f", children={children_repr}" if children_repr else "",
            ">"
        ))


class TargettedParser(HTMLParser):
    """
    Parser de HTML permettant de trouver tous les éléments d’un type
    de balise spécifique avec des attributs spécifiques dans du HTML.
    """

    target_tag: str                             # Le type de balise ciblée
    target_attrs: dict[str, str] | None         # Les attributs et valeurs ciblées, s’il y en a
    _current_elements_stack: list[TagElement]   # Pile d’éléments étant en train d’être parsés
    found_elements: list[TagElement]            # Liste d’éléments correspondant à la cible


    def __init__(self, target_tag: str, target_attrs: dict[str, str] | None = None):
        HTMLParser.__init__(self)
        self.target_tag = target_tag
        self.target_attrs = target_attrs
        self._current_elements_stack = []
        self.found_elements = []


    def is_target(self, tag: str, attrs: list[tuple[str, str | None]]) -> bool:
        """
        Renvoie True si la balise et les attributs
        donnés correspondent à la cible, False sinon.
        """
        # Si la balise n’est pas du bon type, on s’arrête
        if tag != self.target_tag:
            return False
        # Si des attributs cibles sont définis et qu’un des attributs
        # de la balise n’a pas la valeur ciblée, on s’arrête
        if self.target_attrs is not None:
            # Convertit les attributs en un dictionnaire
            attrs_dict = dict(attrs)
            # Pour chaque attribut ciblé
            for target_attr, target_value in self.target_attrs.items():
                # Si l’attribut ciblé n’est pas dans les attributs ou si
                # la valeur de l’attribut n’est pas la bonne, on s’arrête
                value = attrs_dict.get(target_attr)
                if value is None or value != target_value:
                    return False
        return True


    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        """
        Logique :
            si on tombe sur le bon tag :
                on crée un Element, qu’on ajoute à la pile
            sinon :
                si on remplit un élément :
                    on crée un élément et on l’ajoute à la pile
                sinon :
                    on est à l’extérieur donc on fait rien
        """
        # Si la balise correspond à ce qu’on cherche, on crée un nouvel élément
        if self.is_target(tag, attrs):
            # print("BON TAG", tag, attrs)
            self._current_elements_stack.append(TagElement(tag, attrs))
        # Sinon, si on a déjà un élément que l’on remplit, on crée un enfant
        elif self._current_elements_stack:
            # print(f"[+] {tag}, {attrs}")
            self._current_elements_stack.append(TagElement(tag, attrs))
        # else:
        #     print(f"(balise extérieure commencée : {tag})")


    def handle_endtag(self, _: str):
        """
        Logique :
            si on était en train de remplir un élément :
                on finit l’enfant donc on le pop
                tant que la pile contient plus d’un élément :
                    on finit les éléments des niveaux supérieurs donc on les pop tous
                le dernier élément de la pile est le parent donc on le pop et l’ajoute aux résultats
            sinon :
                on est à l’extérieur donc on ne fait rien
        """
        # Si la pile est vide, alors c’est une balise extérieure, on ne fait rien
        if not self._current_elements_stack:
            # print(f"(balise extérieure finie : {tag})")
            return
        # Sinon, on vient de finir soit un enfant, soit un parent
        # Dans tous les cas, on pop le dernier élément
        finished_element = self._current_elements_stack.pop()
        # Si la pile est vide, on vient de finir un parent
        if not self._current_elements_stack:
            # print("FIN BON TAG", finished_element.tag, finished_element.attrs)
            self.found_elements.append(finished_element)
            return
        # Sinon, la pile n’est pas vide, donc on vient de finir un enfant
        # Logiquement, la dernière balise qui a été ouverte doit donc être son parent
        # print(f"[-] {finished_element.tag}, {finished_element.attrs}")
        self._current_elements_stack[-1].children.append(finished_element)


    def handle_data(self, data: str):
        # Si on a des TagElement à remplir et que les données ne sont pas vides
        if self._current_elements_stack and data:
            # On ajoute un ContentElement au dernier TagElement
            self._current_elements_stack[-1].children.append(ContentElement(data))


def flatten_content_of_element(element: TagElement | ContentElement) -> str:
    """
    Retourne le contenu aplati de la balise ou du contenu donné en paramètre,
    c’est-à-dire la valeur de tous les contenus des enfants concaténés.
    """
    if isinstance(element, ContentElement):
        return element.content

    result = ""

    # Pour chaque enfant, aplatit son contenu et concatène le résultat
    for child in element.children:
        flattened_child_content = flatten_content_of_element(child)
        result += flattened_child_content

    return result


def main():
    parser = TargettedParser("balise2", target_attrs={"attribut2": "valeur2"})
    html = "<balise1 attribut1=valeur1><balise2 attribut2=valeur2><balise3 attribut3=valeur3>contenu_balise3</balise3>contenu_balise2</balise2>contenu_balise1</balise1>"

    parser.feed(html)

    print("Éléments trouvés :")
    print(*parser.found_elements, sep="\n\n")

    print("Contenu aplati : ", flatten_content_of_element(parser.found_elements[0]))
    print("Contenu attendu : contenu_balise3contenu_balise2")


if __name__ == "__main__":
    main()
