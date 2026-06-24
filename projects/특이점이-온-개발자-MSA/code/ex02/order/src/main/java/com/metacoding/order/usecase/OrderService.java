package com.metacoding.order.usecase;

import com.metacoding.order.adapter.*;
import com.metacoding.order.adapter.dto.*;
import com.metacoding.order.core.handler.ex.*;
import com.metacoding.order.domain.*;
import com.metacoding.order.repository.*;
import com.metacoding.order.web.dto.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@RequiredArgsConstructor
@Service
@Transactional(readOnly = true)
public class OrderService implements CreateOrderUseCase, GetOrderUseCase, CancelOrderUseCase {

    private final OrderRepository orderRepository;
    private final ProductClient productClient;
    private final DeliveryClient deliveryClient;

    @Override
    @Transactional
    public OrderResponse createOrder(int userId, int productId, int quantity, Long price, String address) {
        // 보상트랜잭션을 위한 변수 선언
        boolean productDecreased = false;
        boolean deliveryCreated = false;
        Order createdOrder = null;

        try {
            // 1. 주문 생성
            createdOrder = orderRepository.save(Order.create(userId, productId, quantity, price));
            createdOrder.validateMinAmount();

            // 2. 상품 재고 차감
            productClient.decreaseQuantity(new ProductRequest(productId, quantity, price));
            productDecreased = true;

            // 3. 배달 생성
            deliveryClient.createDelivery(new DeliveryRequest(createdOrder.getId(), address));
            deliveryCreated = true;

            // 4. 주문 완료
            createdOrder.complete();
            return OrderResponse.from(createdOrder);

        } catch (Exception e) {
            // 배달 취소
            if (deliveryCreated) {
                deliveryClient.cancelDelivery(createdOrder.getId());
            }

            // 재고 복구
            if (productDecreased) {
                productClient.increaseQuantity(new ProductRequest(productId, quantity, price));
            }
            throw new Exception500("주문 생성 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    @Override
    public OrderResponse findById(int orderId) {
        Order findOrder = orderRepository.findById(orderId)
                .orElseThrow(() -> new Exception404("주문을 찾을 수 없습니다."));
        return OrderResponse.from(findOrder);
    }

    @Override
    @Transactional
    public OrderResponse cancelOrder(int orderId) {
        Order findOrder = orderRepository.findById(orderId)
                .orElseThrow(() -> new Exception404("주문을 찾을 수 없습니다."));
        // 상품 재고 복구
        productClient.increaseQuantity(
                new ProductRequest(findOrder.getProductId(), findOrder.getQuantity(), findOrder.getPrice())
        );
        // 배달 취소
        deliveryClient.cancelDelivery(orderId);
        // 주문 취소
        findOrder.cancel();
        return OrderResponse.from(findOrder);
    }
}
