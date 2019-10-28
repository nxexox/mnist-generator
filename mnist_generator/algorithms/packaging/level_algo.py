"""
Level algorithms.

"""
from .base import BasePackagingAlgorithm


class NFLPackingAlgorithm(BasePackagingAlgorithm):
    """
    Next Fit Level.

    """
    def packing(self, rectangles):
        """
        Packing method.

        :param List[Tuple[int, int]] rectangles: List rectangles. Tuple[w, h]

        :return: Array coordinats
        :rtype: List[Tuple[int, int, int, int]]

        const QList<QRect> NFL::pack(const QList<QRect> rects)
        {
            QList<QRect> packed;
            QList<Packager::Level> levels;
            Packager::Level level(0, rects[0].height());

            packed.push_back(level.put(rects[0]));
            levels.push_back(level);

            for (int i = 1; i < rects.size(); i++) {
                if (levels.last().floorFeasible(rects[i])) {
                    packed.push_back(levels.last().put(rects[i]));
                    if (levels.last().height < rects[i].height()) {
                        levels.last().height = rects[i].height();
                    }
                } else {
                    Packager::Level newLevel(levels.last().bottom + levels.last().height,
                                             rects[i].height());
                    packed.push_back(newLevel.put(rects[i]));
                    levels.push_back(newLevel);
                }
            }
            return packed;
        }

        """
        # TODO: https://pastebin.com/eGXRZ65c
        # TODO: https://habr.com/ru/post/160869/
        pass
