import matplotlib.pyplot as plt
import numpy as np
import sklearn.linear_model

# тренировочные данные
X_train = np.random.rand(2000).reshape(1000, 2)*60
y_train = (X_train[:, 0]**2)+(X_train[:, 1]**2)
# тестовые данные
X_test = np.random.rand(200).reshape(100, 2)*60
y_test = (X_test[:, 0]**2)+(X_test[:, 1]**2)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_train[:, 0], X_train[:, 1], y_train, marker='.', color='red')
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_zlabel("Y")

model = sklearn.linear_model.LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

coefs = model.coef_
intercept = model.intercept_
xs = np.tile(np.arange(61), (61, 1))
ys = np.tile(np.arange(61), (61, 1)).T
zs = xs*coefs[0]+ys*coefs[1]+intercept
ax.plot_surface(xs, ys, zs, alpha=0.5)
plt.show()