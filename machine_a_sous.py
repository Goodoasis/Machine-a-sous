# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 19:24:04 2020
@author: Goodoasis
Exercice proposé par Graven www.youtube.com/watch?v=kdvv_3e2yZg&t=4801s
J'ai été un peu plus loin avec une POO et une animation.
"""
import pygame
from numpy import random


class MachineaSous:
    """
    Jeux avec interface graphique.
    Simulant une machine a sous avec 3 images.
    Le joueur fait tourner les images pour avoir les 3 mêmes.
    liste de fruit: ananas, cerise, orange, pasteque, pomme doree.
    Taux d'apparition: 0.4, 0.25, 0.2, 0.10, 0.05
    Récompense : 5, 15, 50, 150 et 10000 jetons
    Le jeu est terminé quand les jetons tombent a 0.

    """

    def __init__(self):
        """
        Constructeur de classe qui initialise la fenetre, créer les variables,
        importe les images et créé=er les widgets.
        """
        pygame.init()
        pygame.display.set_caption("Machine a Sous")
        self.screen = pygame.display.set_mode((730, 480))
        self.background = pygame.Surface(self.screen.get_size())
        self.background_color = (255, 255, 255)
        self.machine_img = pygame.image.load("assets/slot.png")
        self.machine_img_rect = self.machine_img.get_rect()
        # Probabilité pour chaque tile dans l'ordre 0=ananas, 4=pomme_doree.
        self.probability = (0.4, 0.25, 0.2, 0.10, 0.05)
        # Gain pour chaque tile dans l'ordre 0=ananas, 4=pomme_doree.
        self.tile_coin = (5, 15, 50, 150, 10000)
        # Creation des données du joueur.
        self.player_coin = 30
        # Taille des surfaces.
        self._size_slot = (79, 107)

        # Creation des widgets et imports des images.
        self._create_surface()
        self._create_tile()
        self._create_label()

        # Affichage des widegts.
        self._show_widget()

        # Au lancement du jeu affiche 3 fruits au hasard.
        self.launch()

    def play(self):
        """
        Méthode du jeu.
        C'est une boucle qui fait défiler les tuiles.
        A chaque action du joueur, une tuile est selectionnée.
        Au bout de trois, la méthode check_result() est appelée pour vérifier
        si le joueur gagne ou perd la manche.
        Chaque partie coute 1 jeton.
        """
        self.player_money(-1)
        i = 0
        result = []

        while i < 3:
            self.flip()
            if i == 0:
                self.roll(self.list_surface)
            elif i == 1:
                self.roll(self.list_surface[1:])
            elif i == 2:
                self.roll(self.list_surface[2:])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    result.append(self.proba_tile())
                    self.surface_update(self.list_surface[i], tile=result[i])
                    i += 1
                    continue
        self.check_result(result)

    def flip(self):
        """ Rafraichissement de l'affichage global. """
        self.background.fill(self.background_color)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.machine_img, self.machine_img_rect)
        # Affiche les widgets.
        self._show_widget()
        self.label_update()
        pygame.display.flip()

    def _create_tile(self):
        """ Méthode qui importe les images de fruit pour faire les tuiles. """
        # Import des images de fruits qui constituent nos tuiles.
        self.ananas_img = pygame.image.load("assets/ananas.png")
        self.cerise_img = pygame.image.load("assets/cerise.png")
        self.orange_img = pygame.image.load("assets/orange.png")
        self.pasteque_img = pygame.image.load("assets/pasteque.png")
        self.pomme_dore_img = pygame.image.load("assets/pomme_dore.png")
        # Creation des tuples fruit/valeur.
        self.list_tile = (self.ananas_img, self.cerise_img, self.orange_img,
                          self.pasteque_img, self.pomme_dore_img)

    def _create_label(self):
        """ Méthode qui créer le label affichant les jetons du joueur """
        self.coin_img = pygame.image.load("assets/coin.png")
        self.font = pygame.font.SysFont("Arial Black", 45)
        self.yellow = (250, 205, 95)
        # apply it to text on a label
        self.label = self.font.render(f"= {self.player_coin}", 1, self.yellow)

    def _create_surface(self):
        """
        Méthode qui creer les surfaces de la machine a sous qui
        afficherons les fruits. Elle seront contenue dans une liste.
        """
        # Creation des 3 surfaces pour afficher les fruits.
        self.surface_1 = pygame.Surface(self._size_slot)
        self.surface_2 = pygame.Surface(self._size_slot)
        self.surface_3 = pygame.Surface(self._size_slot)
        # Creation de la liste contenant les 3 surfaces.
        self.list_surface = []
        self.list_surface.append(self.surface_1)
        self.list_surface.append(self.surface_2)
        self.list_surface.append(self.surface_3)

    def _show_widget(self):
        """ Méthode qui applique tout les widgets sur la fenetre."""
        # Positions des 3 surfaces.
        slot_1 = (227, 243)
        slot_2 = (328, 242)
        slot_3 = (428, 242)

        # Affiche les surfaces.
        self.screen.blit(self.surface_1, slot_1)
        self.screen.blit(self.surface_2, slot_2)
        self.screen.blit(self.surface_3, slot_3)
        # Affiche l'image de jetons en haut à gauche.
        self.screen.blit(self.coin_img, (10, 18))

    def _img_position(self, surface, img):
        """ Méthode qui permet de centrer une image sur une surface. #fière"""
        # Recupere largeur et hauteur de notre surface.
        surface_width = surface.get_width()
        surface_height = surface.get_height()
        # Recupere largeur et hauteur de notre image.
        img_width = img.get_width()
        img_height = img.get_height()
        # Largeur de surface moins largeur d'image = Centrer l'img sur surface.
        img_posW = (surface_width - img_width) // 2
        img_posH = (surface_height - img_height) // 2
        # retourne le nouveau img.rect.
        img_rect = (img_posW, img_posH, img_width, img_height)
        return img_rect

    def surface_update(self, surface, tile):
        """ Méthode qui affiche une tuile sur une surface."""
        # Remplissage de blanc pour le fond de la surface.
        surface.fill(self.background_color)
        # Affichage de la tuile.
        surface.blit(tile, (self._img_position(surface, tile)))

    def label_update(self):
        """Méthode qui met à jour le label du nombre de jetons de joueur."""
        self.label = self.font.render(f"= {self.player_coin}", 1, self.yellow)
        self.screen.blit(self.label, (80, 15))

    def roll(self, list_surface):
        """
        Méthode qui affiche une tuile au hasard pour
        toutes les surfaces de la liste.
        """
        for surface in list_surface:
            self.surface_update(surface, tile=self.random_tile())

    def random_tile(self):
        """ Méthode qui selectionne une tuile au hasard."""
        # Prend une tuile au hasard.
        tile = random.choice(self.list_tile)
        return tile

    def proba_tile(self):
        """ Méthode qui selectionne une tuile en fonction des probabilités."""
        tile = random.choice(self.list_tile,  p=self.probability)
        return tile

    def player_money(self, amount=0):
        """
        Méthode pour modifier le nombre de jetons du joueur.
        Elle met aussi le Label correspondant à jour.
        """
        if amount != 0:
            self.player_coin += amount
            self.label_update()

    def check_result(self, result):
        """
        Méthode qui vérifie le resultat en comptant le nombre de fois
        que la tuile numéro 1 apparait.
        Si elle apparait 3 fois c'est Win. Elle renvoit ensuite l'index du
        fruit pour que self.gain() compte le montant de jetons gagnés.
        """
        tile = result[0]
        if result.count(tile) == 3:
            index = self.list_tile.index(tile)
            self.gain(win=True, index=index)
        else:
            self.gain()

    def gain(self, win=False, index=None):
        """
        Méthode de fin de partie.
        Si win est True, le nombre de jeton est additionner a la valeur
        du fruit grace a l'index.
        """
        if win:
            self.player_money(self.tile_coin[index])

    def launch(self):
        """ Méthode qui affiche trois fruit au hasard au lancement."""
        self.roll(self.list_surface)

    def main_loop(self):
        """
        La boucle générale de l'appli qui se ferme si l'utilisateur ferme la
        fenetre.
        """
        loop = True
        while loop:
            self.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.player_coin >= 1:
                            self.play()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.machine_img_rect.collidepoint(event.pos):
                        if self.player_coin >= 1:
                            self.play()


APP = MachineaSous()
APP.main_loop()
